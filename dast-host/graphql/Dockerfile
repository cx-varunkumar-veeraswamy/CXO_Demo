FROM node:18-slim
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY server.js .
USER node
EXPOSE 4001
CMD ["node", "server.js"]
