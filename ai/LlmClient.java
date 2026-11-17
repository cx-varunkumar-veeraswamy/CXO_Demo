// INTENTIONALLY INSECURE LLM CLIENT (Java) - AI Supply Chain Security demo only. Keys are fake.
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.model.azure.AzureOpenAiChatModel;
import dev.langchain4j.model.anthropic.AnthropicChatModel;
import dev.langchain4j.model.googleai.GoogleAiGeminiChatModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.model.mistralai.MistralAiChatModel;
import javax.servlet.http.*;
import java.io.IOException;

public class LlmClient extends HttpServlet {
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String prompt = req.getParameter("prompt");                                   // untrusted prompt
        String out = OpenAiChatModel.builder().apiKey("sk-proj-FAKEFAKEFAKEFAKEFAKEFAKEFAKE").modelName("gpt-4o").build().generate(prompt)
          + AzureOpenAiChatModel.builder().apiKey("FAKEAZUREKEY0000").endpoint("https://cxo.openai.azure.com").deploymentName("gpt-35-turbo").build().generate(prompt)
          + AnthropicChatModel.builder().apiKey("sk-ant-api03-FAKEFAKE").modelName("claude-3-opus-20240229").build().generate(prompt)
          + GoogleAiGeminiChatModel.builder().apiKey("AIzaSyFAKEFAKEFAKEFAKE").modelName("gemini-1.5-pro").build().generate(prompt)
          + MistralAiChatModel.builder().apiKey("FAKEMISTRAL").modelName("open-mixtral-8x22b").build().generate(prompt)
          + OllamaChatModel.builder().baseUrl("http://localhost:11434").modelName("codellama").build().generate(prompt);
        resp.getWriter().println(out);                                                // LLM output reflected unsanitised (XSS)
    }
}
