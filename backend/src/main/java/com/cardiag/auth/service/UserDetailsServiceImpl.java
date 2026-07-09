package com.cardiag.auth.service;

import com.cardiag.auth.entity.User;
import com.cardiag.auth.repository.UserRepository;
import com.cardiag.common.exception.BusinessException;
import com.cardiag.common.security.UserPrincipal;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserDetailsServiceImpl implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new BusinessException("User not found"));
        return new UserPrincipal(user);
    }
}
