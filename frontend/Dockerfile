FROM node:22 AS builder
COPY . /app/
WORKDIR /app
RUN yarn install
RUN yarn build
RUN mv /app/.output /app/build
RUN yarn generate
RUN cp -rf /app/build/* /app/.output

FROM node:22
LABEL author="Owain Jones <github.com/erinaceous>"
WORKDIR /app
EXPOSE 80
ENTRYPOINT [ "node", "/app/server/index.mjs" ]
RUN useradd -d /app -m user && chown -R user:user /app
USER user
COPY --from=builder /app/build /app/
