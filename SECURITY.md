# Security

RiseWell is a coursework prototype and has not undergone a production security review. Use synthetic data in a private test environment.

## Before a public deployment

- Add device authentication and authorization to alarm-history ingestion. A client-supplied user ID is not proof of identity.
- Protect the speech-generation endpoint with authentication, rate limits, and usage controls before exposing a paid API key through it.
- Remove or restrict the generic `/api/data` and `/api/alarm-history/seed` demo routes.
- Scope heart-rate reads to the authenticated user. The current endpoint checks sign-in but reads all users’ readings.
- Review all remaining routes for authorization, input limits, and data isolation. Clerk middleware by itself does not require sign-in.
- Review dependency advisories and upgrade unsupported or vulnerable packages before public hosting.
- Replace the RabbitMQ development credentials before any remote use and restrict its network ports.

## Previously exposed configuration

The original repository contained a database credential in tracked source/configuration. Removing it from the working tree does not remove it from Git history or existing clones. The owner should revoke/rotate the credential, review database access, and decide whether history cleanup is needed. The original project report also contained a shared demo login; retire that account or rotate its password. Do not republish that login in documentation.

## Reporting

Use the repository’s private vulnerability reporting feature if enabled, or contact a maintainer privately. Do not put credentials, personal data, or exploitable details in a public issue.
