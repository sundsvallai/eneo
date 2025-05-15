FROM node:20-bullseye-slim AS base

# Stage 1: Get turbo and prepare docker prune/build
FROM base AS builder
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
# https://github.com/pnpm/pnpm/issues/9029
RUN npm i -g corepack@latest
RUN corepack enable

WORKDIR /app
COPY . .
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

# Stage 3: Run app
# Required ENV vars, see README.md
# ORIGIN, JWT_SECRET, PUBLIC_API_URL
FROM base AS runner
WORKDIR /app
COPY --from=builder /app/apps/web/build build/
COPY --from=builder /app/apps/web/package.json .
EXPOSE 3000
USER node
ENV NODE_ENV="production"
CMD ["node", "build"]
