package demo.api;

import java.util.List;
import javax.persistence.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

/** INTENTIONALLY INSECURE Spring REST API - sensitive data exposure + modifiable source data. Demo only. */
@RestController
@RequestMapping("/api/users")
public class UserApiController {
    @Autowired UserRepository repo;                 // Spring Data JPA repository
    @Autowired JdbcTemplate jdbc;

    @Entity
    public static class User {                      // entity exposed directly as the API model
        @Id public Long id;
        public String username, password, ssn, email, phone, address, creditCard, role;
        public long balance;
    }

    @GetMapping("/{id}")
    public User get(@PathVariable Long id) { return repo.findById(id).get(); }       // returns SSN, card, password; no ownership check (BOLA)

    @GetMapping
    public List<User> all() { return repo.findAll(); }                              // bulk PII exposure

    @PutMapping("/{id}")
    public User update(@PathVariable Long id, @RequestBody User body) {            // mass assignment: client sets role/balance
        body.id = id;
        return repo.save(body);
    }

    @GetMapping("/search")
    public List<?> search(@RequestParam String q) {                                 // SQLi reaches the sensitive table
        return jdbc.queryForList("SELECT * FROM users WHERE username LIKE '%" + q + "%'");
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) { repo.deleteById(id); }              // no authorization
    interface UserRepository extends org.springframework.data.jpa.repository.JpaRepository<User, Long> {}
}
