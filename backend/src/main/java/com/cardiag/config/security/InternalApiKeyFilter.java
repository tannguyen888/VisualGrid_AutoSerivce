package com.cardiag.config.security;

import com.cardiag.config.AiProperties;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

/**
 * Authenticates machine-to-machine calls from AI_service to /api/ai/** using a
 * shared secret header instead of the normal user JWT flow.
 */
@Component
@RequiredArgsConstructor
public class InternalApiKeyFilter extends OncePerRequestFilter {

    private static final String HEADER = "X-Internal-Api-Key";

    private final AiProperties aiProperties;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String key = aiProperties.getBackendApiKey();
        String header = request.getHeader(HEADER);

        if (request.getRequestURI().startsWith("/api/ai/") && key != null && !key.isBlank() && key.equals(header)) {
            SecurityContextHolder.getContext().setAuthentication(
                    new UsernamePasswordAuthenticationToken(
                            "ai-service", null, List.of(new SimpleGrantedAuthority("ROLE_SERVICE"))));
        }

        chain.doFilter(request, response);
    }
}
