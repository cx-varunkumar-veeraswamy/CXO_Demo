// INTENTIONALLY VULNERABLE GraphQL API (hosted variant) for Checkmarx DAST demos.
// Flaws: introspection on, no depth/complexity limits, no auth, SQLi, sensitive fields, batching, CORS *.
const { ApolloServer, gql } = require('apollo-server');
const initSqlJs = require('sql.js');

const typeDefs = gql`
  type User { id: ID! username: String! password: String! ssn: String role: String }
  type Query {
    user(id: ID!): [User]
    users(limit: Int): [User]
    search(q: String): [User]
  }
  type Mutation {
    updateUser(id: ID!, role: String, password: String): Boolean
    deleteUser(id: ID!): Boolean
  }
`;

(async () => {
  const SQL = await initSqlJs();
  const db = new SQL.Database();
  db.run("CREATE TABLE users(id INTEGER, username TEXT, password TEXT, ssn TEXT, role TEXT)");
  db.run("INSERT INTO users VALUES (1,'admin','admin','123-45-6789','admin'),(2,'bob','bob','987-65-4321','user')");
  const q = (sql) => {
    const r = db.exec(sql);
    if (!r.length) return [];
    return r[0].values.map(v => Object.fromEntries(r[0].columns.map((c, i) => [c, v[i]])));
  };
  const resolvers = {
    Query: {
      user: (_, { id }) => q(`SELECT * FROM users WHERE id=${id}`),                         // SQLi + BOLA
      users: (_, { limit }) => q(`SELECT * FROM users LIMIT ${limit || 100}`),
      search: (_, { q: s }) => q(`SELECT * FROM users WHERE username LIKE '%${s}%'`),
    },
    Mutation: {
      updateUser: (_, { id, role, password }) => { db.run(`UPDATE users SET role='${role}' WHERE id=${id}`); return true; },
      deleteUser: (_, { id }) => { db.run(`DELETE FROM users WHERE id=${id}`); return true; },
    },
  };
  new ApolloServer({ typeDefs, resolvers, introspection: true, debug: true, cors: { origin: '*' } })
    .listen({ port: 4001, host: '0.0.0.0' }).then(({ url }) => console.log('GraphQL at ' + url));
})();
