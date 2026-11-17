// INTENTIONALLY VULNERABLE GraphQL server - demo only.
const { ApolloServer } = require('apollo-server');
const fs = require('fs');
const { exec } = require('child_process');
const db = require('./db');

const server = new ApolloServer({
  typeDefs: fs.readFileSync('./schema.graphql', 'utf8'),
  resolvers: {
    Query: {
      user: (_, { id }) => db.query(`SELECT * FROM users WHERE id=${id}`),       // SQLi + BOLA
      search: (_, { q }) => db.query(`SELECT * FROM users WHERE name LIKE '%${q}%'`),
      users: (_, { limit }) => db.query(`SELECT * FROM users LIMIT ${limit}`),   // no pagination cap
    },
    Mutation: {
      runCommand: (_, { cmd }) => new Promise(r => exec(cmd, (e, o) => r(o))),   // RCE
    },
  },
  introspection: true, playground: true, debug: true, cors: { origin: '*' },     // no limits, no auth
});
server.listen(4001);
