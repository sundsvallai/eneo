# Deployment

intric can be run with Docker. We recommend [Docker Compose](https://docs.docker.com/compose/).

## System requirements

intric requires PostgreSQL (13+), Redis, a web service, and a worker service.

Since intric uses [pgvector](https://github.com/pgvector/pgvector) as its vector database, the memory requirements are dwarfed compared to keeping a HNSW constantly in memory.

* Recommended system requirements: 4GB RAM
* Minimum system requirements: 1GB RAM

Disk usage is mostly affected by the amount of embedded documents, as the embeddings dwarf all other stored information. As a rough guide, you can expect a 25x multiplier on the embeddded information. That is, if you have 1MB of text data in your knowledge, that means that you also have about 25MB of vector data.

## Connectivity

intric requires that outgoing traffic is allowed in order to query the LLMs. Inbound traffic should only require port 443 to be open, however consider also allowing ssh.

## Production considerations

When running intric in production, make sure that you think about the following:

1. Restarts: Ensure that the application can handle restarts gracefully, possibly due to crashes or updates.
2. Monitoring: Implement monitoring to keep track of the application's performance and health.
3. Backups: Regularly back up data to prevent data loss in case of failures.
4. SSL/TLS termination: Secure the application by using SSL/TLS to encrypt data in transit.
5. Environment configuration: Properly configure the environment variables.

Consider dockerizing the application in order to ensure consistent environments across different deployment stages. This helps in minimizing discrepancies between development, staging, and production environments.