FROM node:20 AS builder
COPY . /app/
WORKDIR /app
RUN yarn install
RUN yarn build

FROM node:20
LABEL author="Owain Jones <github.com/erinaceous>"
WORKDIR /app
EXPOSE 80
ENTRYPOINT [ "node", "/app/server/index.mjs" ]
RUN useradd -d /app -m user && chown -R user:user /app
USER user
COPY --from=builder /app/.output /app/
