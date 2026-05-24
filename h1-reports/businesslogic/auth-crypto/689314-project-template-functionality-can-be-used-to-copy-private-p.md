# Project Template functionality can be used to copy private project data, such as repository, confidential issues, snippets, and merge requests

## Metadata
- **Source:** HackerOne
- **Report:** 689314 | https://hackerone.com/reports/689314
- **Submitted:** 2019-09-06
- **Reporter:** jobert
- **Program:** Unknown
- **Bounty:** $12,000
- **Severity:** critical
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I've found a three minor vulnerabilities which, when combined, allow an attacker to copy private repositories, confidential issues, private snippets, and then some. I'll go through the code path to explain the vulnerabilities and how they are combined. See the **Proof of Concept** section if you want to reproduce it immediately.

Let's start at the `ProjectsController` of EE, which is prepended to

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

I've found a three minor vulnerabilities which, when combined, allow an attacker to copy private repositories, confidential issues, private snippets, and then some. I'll go through the code path to explain the vulnerabilities and how they are combined. See the **Proof of Concept** section if you want to reproduce it immediately.

Let's start at the `ProjectsController` of EE, which is prepended to `app/controllers/projects_controller.rb` in an EE instance. 

**ee/app/controllers/ee/projects_controller.rb**
```ruby
override :project_params_attributes
    def project_params_attributes
      super + project_params_ee
    end

def project_params_ee
  attrs = %i[
    # ...
    use_custom_template
    # ...
    group_with_project_templates_id
  ]

  # ...

  attrs
end
```

This method defines what parameters can be passed by the user. The two notable parameters here are `use_custom_template` and `group_with_project_templates_id`. This method appends the result value of `project_params_attributes` method in `app/controllers/projects_controller.rb` on line 351, which specifies all the CE attributes a user can provide when creating a project. The CE controller allows the `template_name` parameter to be passed, too. This means that these three parameters can be passed to the `Projects::CreateService` in the `create` method:

**app/controllers/projects_controller.rb**
```ruby
def create
  @project = ::Projects::CreateService.new(current_user, project_params(attributes: project_params_create_attributes)).execute

  # ...
end

# ...

def project_params_attributes
  [
    # ...
    :template_name,
    # ...
  ]
```

In EE, the `EE:Projects::CreateService` is prepended to the `Projects::CreateService`. The prepended EE code contains logic to validate the `use_custom_template` and `group_with_project_templates_id` parameters.

**ee/app/services/ee/projects/create_service.rb**
```ruby
def execute
  # ...

  group_with_project_templates_id = params.delete(:group_with_project_templates_id) if params[:template_name].blank?

  # ...

    validate_namespace_used_with_template(project, group_with_project_templates_id)
end

# ...

def validate_namespace_used_with_template(project, group_with_project_templates_id)
  return unless project.group

  subgroup_with_templates_id = group_with_project_templates_id || params[:group_with_project_templates_id]
  return if subgroup_with_templates_id.blank?

  templates_owner = ::Group.find(subgroup_with_templates_id).parent

  unless templates_owner.self_and_descendants.exists?(id: project.namespace_id)
    project.errors.add(:namespace, _("is not a descendant of the Group owning the template"))
  end
end
```

The code above is where the first vulnerability can be found. In a normal situation, a Project Template can only be copied to a namespace (group) that is a descendant of the project template. However, the `validate_namespace_used_with_template` method returns a `nil` value when the project is **not** being created for a group (`return unless project.group`). This means that if a `group_with_project_templates_id` is given for a project that is created in a `User` namespace, the authorization / validation logic is never executed. This means that the `use_custom_template` and `group_with_project_templates_id` parameters remain to be set on the instance variable `params`.

Because the EE code is prepended, the `execute` method is executed before the `Projects::CreateService` is called. Because the EE class its validation logic is bypassed, the `execute` method of the `Projects::CreateService` class is called:

**app/services/projects/create_service.rb**
```ruby
def execute
  if @params[:template_name].present?
    return ::Projects::CreateFromTemplateService.new(current_user, params).execute
  end

  # ...
end
```

When a `template_name` is given, instead of executing the normal execution flow, the result of `Projects::CreateFromTemplateService` is returned. The CE code for this class isn't very important. The EE class contains the logic that is worth checking out:

**ee/app/services/ee/projects/create_from_template_service.rb**
```ruby
def execute
  return super unless use_custom_template?

  override_params = params.dup
  params[:custom_template] = template_project if template_project

  ::Projects::GitlabProjectsImportService.new(current_user, params, override_params).execute
end

private

def use_custom_template?
  # ...
    template_name &&
      ::Gitlab::Utils.to_boolean(params.delete(:use_custom_template)) &&
      ::Gitlab::CurrentSettings.custom_project_templates_enabled?
  # ...
end

def template_project
  # ...
    current_user.available_custom_project_templates(search: template_name, subgroup_id: subgroup_id)
                .first
  # ...
end

def subgroup_id
  params[:group_with_project_templates_id].presence
end
```

This class does a couple of things: it makes sure a custom template name is given, that it should use the given template name, and that the GitLab instance has custom project templates enabled. For what it's worth: gitlab.com has this setting enabled. When it passes those checks, the `template_project` method is invoked. Here is the definition of the `available_custom_project_templates` method:

**ee/app/models/ee/user.rb**
```ruby
def available_custom_project_templates(search: nil, subgroup_id: nil)
  templates = ::Gitlab::CurrentSettings.available_custom_project_templates(subgroup_id)

  ::ProjectsFinder.new(current_user: self,
                       project_ids_relation: templates,
                       params: { search: search, sort: 'name_asc' })
                  .execute
end
```

This method requires two parameters: `search` and `subgroup_id`. The first one is the `template_name` the user passes, the second one `group_with_project_templates_id`. The `templates` variable gets its value based on the following method definition:

**ee/app/models/ee/application_setting.rb**
```ruby
def available_custom_project_templates(subgroup_id = nil)
  group_id = subgroup_id || custom_project_templates_group_id

  return ::Project.none unless group_id

  ::Project.where(namespace_id: group_id) 
end
```

This method will return all `Project` models based on the `namespace_id` that is provided in the `subgroup_id` parameter. This is then passed to the `ProjectsFinder` in the `available_custom_project_templates` method on the `User` model. This is where the second vulnerability can be found. The `ProjectsFinder` uses an initial collection, which consists of the projects the authenticated user can access. However, it does **not** check the access level of the user. This means that any project that is public, but has Repository, Issue, Snippets (etc.) access disabled for Guests, will be returned by the `available_custom_project_templates` method on the `User` model. In a perfect world, it seems that this method would limit the projects that can be returned based on the user's permissions for said projects.

If we go back to the `EE:Projects::CreateFromTemplateService` file, you can see that the `template_project` will return the first project that is returned by the `available_custom_project_templates` method. This means that `params[:custom_template]` may contain a `Project` model that the user is not authorized to see everything for. The `EE::Projects::CreateFromTemplateService` class then calls the `Projects::GitlabProjectsImportService` class with the updated parameters.

**ee/app/services/ee/projects/gitlab_projects_import_service.rb**
```ruby
def execute
  super.tap do |project|
    if project.saved? && custom_template
      custom_template.add_export_job(current_user: current_user,
                                     after_export_strategy: export_strategy(project))
    end
  end
end

private

override :prepare_import_params
def prepare_import_params
  super

  if custom_template
    params[:import_type] = 'gitlab_custom_project_template'
  end
end

def custom_template
  strong_memoize(:custom_template) do
   

</details>

---
*Analysed by Claude on 2026-05-24*
