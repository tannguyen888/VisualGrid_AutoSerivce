package com.cardiag.controller;

import com.cardiag.service.AiService;
import com.cardiag.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiService aiService;

    @GetMapping("/analyze")
    public ResponseEntity<ApiResponse<String>> analyze(@RequestParam String input) {
        return ResponseEntity.ok(ApiResponse.success("AI analysis generated", aiService.analyzeDiagnostic(input)));
    }
}
