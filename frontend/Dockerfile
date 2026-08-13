# syntax=docker/dockerfile:1
# ── Frontend image: node build stage → nginx serve stage ──────────────────────
# Bases digest-pinned (freezes the tested rebuild; bump deliberately + make verify).
# Dependency layer isolated: editing src/ never re-runs npm ci; npm cache mounted.
FROM node:20-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0 AS build
WORKDIR /build
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY index.html vite.config.ts tsconfig.json ./
COPY src/ src/
RUN npm run build

FROM nginx:1.27-alpine@sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /build/dist /usr/share/nginx/html
