package demo;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.context.annotation.Bean;

/** INTENTIONALLY INSECURE Spring Security config - demo only. */
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()                                  // VULN-340 CSRF protection disabled
            .headers().frameOptions().disable()                // VULN-341 clickjacking protection disabled
            .httpStrictTransportSecurity().disable()           // VULN-342 HSTS disabled
            .and().authorizeRequests().antMatchers("/**").permitAll()  // VULN-343 no authentication on any route
            .and().sessionManagement().sessionFixation().none();       // VULN-344 session fixation protection off
    }
    @Bean
    public PasswordEncoder encoder() { return NoOpPasswordEncoder.getInstance(); }  // VULN-345 plaintext passwords
}
