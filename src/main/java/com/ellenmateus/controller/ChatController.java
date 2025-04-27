package com.ellenmateus.controller;

import com.ellenmateus.model.ChatMessage;
import com.ellenmateus.repository.ChatMessageRepository;
import com.ellenmateus.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import java.util.List;

@Controller
@RequestMapping("/chat")
public class ChatController {

    private final ChatService chatService;
    private final ChatMessageRepository chatRepo;

    @Autowired
    public ChatController(ChatService chatService,
                          ChatMessageRepository chatRepo) {
        this.chatService = chatService;
        this.chatRepo = chatRepo;
    }

    /** Serve a página Thymeleaf em GET /chat */
    @GetMapping
    public String showChatPage(Model model) {
        List<ChatMessage> history = chatRepo.findAll();
        model.addAttribute("messages", history);
        return "chat";  // vai renderizar src/main/resources/templates/chat.html
    }

    /**
     * API que recebe JSON { "userMessage": "..." }
     * e retorna o ChatMessage completo com botResponse e timestamp.
     */
    @PostMapping("/ask")
    @ResponseBody
    public ResponseEntity<ChatMessage> ask(@RequestBody ChatMessage incoming) {
        String userMsg = incoming.getUserMessage();
        // Chama seu serviço que faz o POST ao GPT4All e retorna a resposta dinâmica
        String botReply = chatService.ask(userMsg);

        // Cria e salva no banco de dados
        ChatMessage saved = new ChatMessage(userMsg, botReply);
        chatRepo.save(saved);

        // Retorna o objeto completo
        return ResponseEntity.ok(saved);
    }
}
