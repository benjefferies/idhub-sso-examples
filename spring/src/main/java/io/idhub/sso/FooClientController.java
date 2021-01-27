package io.idhub.sso;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.security.Principal;

@Controller
public class FooClientController {

    @GetMapping("/foos")
    public String getFoos(Model model, Principal principal) {
        return "foos";
    }
}
