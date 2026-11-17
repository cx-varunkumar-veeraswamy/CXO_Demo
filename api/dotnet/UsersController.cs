// INTENTIONALLY INSECURE ASP.NET Core Web API - sensitive data exposure + modifiable source data. Demo only.
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Demo.Api
{
    public class User
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string PasswordHash { get; set; }
        public string Ssn { get; set; }
        public string Email { get; set; }
        public string CreditCard { get; set; }
        public string Role { get; set; }
        public decimal Balance { get; set; }
    }
    public class Db : DbContext { public DbSet<User> Users { get; set; } }

    [ApiController, Route("api/users")]
    public class UsersController : ControllerBase
    {
        private readonly Db _db = new Db();

        [HttpGet("{id}")]
        public User Get(int id) => _db.Users.Find(id);                                         // entity returned as-is: SSN, card, hash; no ownership check

        [HttpGet]
        public IQueryable<User> All() => _db.Users;                                            // bulk PII

        [HttpPut("{id}")]
        public IActionResult Update(int id, [FromBody] User body)                              // over-posting: Role/Balance bound from client
        {
            body.Id = id; _db.Update(body); _db.SaveChanges(); return Ok(body);
        }

        [HttpGet("search")]
        public object Search(string q) => _db.Users.FromSqlRaw("SELECT * FROM Users WHERE Username LIKE '%" + q + "%'").ToList(); // SQLi
    }
}
