# --- Stage 1: Build Stage ---
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json yarn.lock* package-lock.json* ./

# Install build dependencies
RUN yarn install --frozen-lockfile || npm install

# Copy all source code
COPY . .

# Build the Next.js app
RUN yarn build

# --- Stage 2: Production/Runtime Stage ---
FROM node:20-alpine

WORKDIR /app

# Copy built app and node_modules
COPY --from=builder /app/ ./

EXPOSE 3000

# Start the Next.js app
CMD ["yarn", "start"]
