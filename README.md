# CXO Demo – Intentionally Vulnerable Application

> **WARNING:** Every file here is deliberately insecure and exists only to showcase **Checkmarx One** scanners.
> Never deploy it to a real environment or expose it to the internet. All secrets/keys are fake.

## Layout → Checkmarx One scanner mapping

| Folder | Scanner | What it demonstrates |
|---|---|---|
| `sast/<language>/` | **SAST** (+ **SCA** via manifests) | 23 language modules: Java, C#, Python, JavaScript, TypeScript, PHP, Go, Ruby, Kotlin, Swift, Scala, C, C++, Groovy, Perl, Rust, Apex, PL/SQL, Dart, VB.NET, Classic ASP, Objective-C. Each file has `VULN-nnn` tags (171 tagged findings): SQLi, XSS, command/code injection, SSTI, XXE, SSRF, path traversal, open redirect, insecure deserialization, weak crypto/hash/PRNG, hardcoded creds, buffer overflow, use-after-free, format string, prototype pollution, NoSQLi, LDAP injection, LFI/RFI, unrestricted upload, etc. |
| `sast/*/pom.xml`, `package.json`, `requirements.txt`, `go.mod`, `Gemfile`, `composer.json`, `Cargo.toml`, `*.csproj`, `build.gradle`, `build.sbt`, `pubspec.yaml`, `Podfile` | **SCA** | Old/vulnerable OSS packages across 12 ecosystems (log4j 2.14.1, Spring 5.3.17, Struts 2.5.25, lodash 4.17.15, Django 2.2.0, Newtonsoft 9.0.1, …). |
| `iac/` | **IaC Security** | Terraform (AWS/Azure/GCP), CloudFormation, Kubernetes, Helm, Ansible, ARM, Bicep, Google Deployment Manager, Serverless, Pulumi, Crossplane. |
| `containers/` | **Containers** + IaC (Dockerfile/Compose) | 7 Dockerfiles with EOL base images, root user, secrets in ENV/ARG, curl-pipe-sh, exposed SSH; privileged Compose. |
| `api/` | **API Security / DAST** | REST (Flask, OWASP API Top 10), OpenAPI spec, gRPC (.proto + server), GraphQL, SOAP/WSDL, WebSocket, Postman collection. |
| `ai/` | **AI Supply Chain Security** | 15 Hugging Face models from Meta, Mistral, Google, Microsoft, Alibaba, DeepSeek, TII, Stability, BigScience, EleutherAI, Salesforce, BigCode, 01.AI, NVIDIA + unvetted community model; plus OpenAI, Anthropic, Google Gemini, Cohere, Mistral API, Replicate, AWS Bedrock (Titan), Azure OpenAI; `trust_remote_code`, pickle/`torch.load`, LLM-output `exec`, agent excessive agency. |
| `secrets/` | **Secret Detection** | Fake AWS/GitHub/Slack/Stripe/SendGrid/Twilio/Google/Azure/NPM/GitLab/Docker tokens, DB URLs, RSA private key, passwords in properties/shell. |

## Running the scan
1. Push this folder to the GitHub repository mapped to your Checkmarx One project.
2. In Checkmarx One, enable all engines: **SAST, SCA, IaC Security, Containers, Secret Detection, API Security, AI Supply Chain Security (Supply Chain)**.
3. For **DAST**, run `api/rest-server/server.py` (`pip install flask flask-cors pyjwt requests`) inside an isolated lab VM/container and point the DAST scan at `http://<host>:8000` using `api/openapi/openapi.yaml`.
4. For Containers scans, build images (`docker build -f containers/Dockerfile.python .`) or let Checkmarx scan the Dockerfiles/Compose directly.

## Notes
- Counts are of *distinct vulnerability classes/rules*; the same class appearing in several languages yields separate findings.
- Real findings depend on the scanner version and your project's presets; use the *All* preset for the richest results.
- Source is not required to compile; it is written to be recognisable by static analysis.

> Scans run automatically via GitHub Actions (`.github/workflows/main.yml`) on every push to `main`.

