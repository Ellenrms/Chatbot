package com.ellenmateus.service;

import com.ellenmateus.dto.ChatRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class ChatService {
    private static final Logger log = LoggerFactory.getLogger(ChatService.class);

    private final RestTemplate rest;
    private final String gptServerUrl;
    private final ObjectMapper mapper = new ObjectMapper();

    public ChatService(RestTemplate restTemplate,
                       @Value("${chat.gpt.url}") String gptServerUrl) {
        this.rest = restTemplate;
        this.gptServerUrl = gptServerUrl;
    }

    // Parâmetro renomeado para userQuestion
    public String ask(String userQuestion) {
        try {
            // Instrução para o modelo LLM (engenharia de prompt)
            String systemContext = "Você é um chatbot especializado em ensinar programação Java para iniciantes. Por favor, explique o seguinte conceito de Java de forma clara, concisa e com exemplos simples se possível: ";
            String finalPromptToLLM = systemContext + userQuestion;

            // Usar finalPromptToLLM e aumentar maxNewTokens para 300
            ChatRequest req = new ChatRequest(finalPromptToLLM, 300); 
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<ChatRequest> entity = new HttpEntity<>(req, headers);

            // Log do prompt completo que está sendo enviado
            log.info("Enviando prompt completo para LLM: {}", finalPromptToLLM);
            
            ResponseEntity<String> respEntity = rest.exchange(
                    gptServerUrl,
                    HttpMethod.POST,
                    entity,
                    String.class
            );
            String rawJson = respEntity.getBody();
            log.info("Resposta bruta do GPT4All: {}", rawJson);

            JsonNode root = mapper.readTree(rawJson);
            JsonNode results = root.path("results");
            if (results.isArray() && results.size() > 0) {
                String text = results.get(0).path("text").asText();
                return text.trim();
            }
        } catch (Exception e) {
            log.error("Erro ao chamar GPT4All", e);
        }
        return "Desculpe, não consegui gerar uma resposta.";
    }
}