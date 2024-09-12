# intric backend

## Environment variables

| Variable                         | Required | Explanation                                 |
|----------------------------------|----------|---------------------------------------------|
| OPENAI_API_KEY                   |          | Api key for openai                          |
| ANTHROPIC_API_KEY                |          | Api key for anthropic                       |
| AZURE_API_KEY                    |          | Api key for azure                           |
| AZURE_MODEL_DEPLOYMENT           |          | Deployment for azure                        |
| AZURE_ENDPOINT                   |          | Endpoint for azure                          |
| AZURE_API_VERSION                |          | Api version for azure                       |
| POSTGRES_USER                    | x        |                                             |
| POSTGRES_PASSWORD                | x        |                                             |
| POSTGRES_PORT                    | x        |                                             |
| POSTGRES_HOST                    | x        |                                             |
| POSTGRES_DB                      | x        |                                             |
| REDIS_HOST                       | x        |                                             |
| REDIS_PORT                       | x        |                                             |
| MOBILITYGUARD_DISCOVERY_ENDPOINT |          |                                             |
| MOBILITYGUARD_CLIENT_ID          |          |                                             |
| MOBILITYGUARD_CLIENT_SECRET      |          |                                             |
| UPLOAD_FILE_TO_SESSION_MAX_SIZE  | x        |                                             |
| UPLOAD_IMAGE_TO_SESSION_MAX_SIZE | x        |                                             |
| UPLOAD_MAX_FILE_SIZE             | x        | Max file size for uploading to a collection |
| TRANSCRIPTION_MAX_FILE_SIZE      | x        | Max file size for uploading to a collection |
| MAX_IN_QUESTION                  | x        | Max files in a question                     |
| USING_ACCESS_MANAGEMENT          |          | Feature flag if using access management     |
| USING_AZURE_MODELS               |          | Feature flag if using azure models          |
| API_PREFIX                       | x        | Api prefix - eg `/api/v1/`                  |
| API_KEY_LENGTH                   | x        | Length of the generated api keys            |
| API_KEY_HEADER_NAME              | x        | Header name for the api keys                |
| JWT_AUDIENCE                     | x        |                                             |
| JWT_ISSUER                       | x        |                                             |
| JWT_EXPIRY_TIME                  | x        | In seconds                                  |
| JWT_ALGORITHM                    | x        |                                             |
| JWT_SECRET                       | x        |                                             |
| JWT_TOKEN_PREFIX                 | x        | In the header - eg `Bearer`                 |
| LOGLEVEL                         |          | one of ´INFO´, ´DEBUG´, ´WARNING´, ´ERROR´  |