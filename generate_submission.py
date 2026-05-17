from fpdf import FPDF
import zipfile
import os

STUDENT_ID = "22-101092_21-101105_21-101080"
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ProvenanceGate Technical Report", ln=True, align='C')
    pdf.ln(10)
    
    # Section 1: Architecture/Design
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="1. Architecture and Design", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="ProvenanceGate is an anti-prompt-injection framework designed to protect Large Language Models (LLMs) from malicious inputs, specifically in Retrieval-Augmented Generation (RAG) and Agentic architectures. The system is built around a Context Assembler and a Policy Engine. The Context Assembler assigns explicit trust levels (e.g., SYSTEM, USER, RETRIEVED, TOOL) to different input chunks. The architecture organizes context so that higher-trust prompts (like system instructions) take precedence. The Policy Engine enforces strict security rules by scanning lower-trust chunks for instruction-overriding patterns (e.g., 'ignore previous instructions').")
    pdf.ln(5)
    
    # Section 2: Implementation Details
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="2. Implementation Details", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="The core implementation consists of the following components:\n- assembler.py: Defines the 'Trust' enum and 'Chunk' class. It collects input segments and sorts them by trust level, generating structured prompt messages.\n- policy.py: Contains the 'PolicyEngine' class which scans untrusted chunks for predefined adversarial patterns. It raises a 'PolicyViolation' if an injection attempt is detected.\n- mock_llm.py: A deterministic, offline mock for the google.genai.Client, which allows the system to be tested safely and without API credentials.\n- main.py: Orchestrates the workflow, managing the assembler and policy engine, and invoking the LLM if the request is deemed safe.\n- rag_demo.py: Demonstrates naive RAG versus ProvenanceGate-protected RAG using simulated clean and poisoned documents.")
    pdf.ln(5)
    
    # Section 3: Testing & Results
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="3. Testing and Results", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="The framework was successfully tested using local demonstration scripts. The test environment successfully executed 'main.py' and 'rag_demo.py'.\nResults:\n- Clean Interaction: The LLM accurately summarized data without triggering the policy engine.\n- Injection Attempt (Strict Mode): When a document containing 'ignore previous instructions' was injected, the Policy Engine correctly identified the pattern in a lower-trust chunk and raised a PolicyViolation, effectively blocking the attack.\n- Injection Attempt (Non-Strict Mode): Demonstrated the system's susceptibility when strict mode is disabled, allowing adversarial instructions to bleed into the model's context.")
    pdf.ln(5)
    
    # Section 4: Discussion
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="4. Discussion", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Challenges Faced: The main challenge was ensuring that the Policy Engine correctly distinguishes between benign user instructions and adversarial overrides without high false-positive rates.\nSecurity Implications: The chunk-based trust level approach significantly mitigates the risk of direct prompt injection in RAG scenarios. By explicitly separating system context from retrieved data, the LLM is less likely to be hijacked.\nLimitations: The current policy relies on pattern matching (keyword-based heuristics) which can be bypassed by semantically fluent, non-standard injection patterns (e.g., perplexity detection failures). Future iterations could incorporate an LLM-based evaluator for analyzing intent.")
    pdf.ln(5)
    
    report_filename = f"{STUDENT_ID}_Project_Report.pdf"
    pdf.output(report_filename)
    return report_filename

def create_zip(zip_filename):
    files_to_zip = [
        "assembler.py",
        "main.py",
        "mock_llm.py",
        "policy.py",
        "rag_demo.py",
        "requirements.txt",
        "README.md"
    ]
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
    return zip_filename

if __name__ == "__main__":
    pdf_file = generate_pdf()
    print(f"Generated PDF: {pdf_file}")
    zip_file = create_zip(f"{STUDENT_ID}_Project_Code.zip")
    print(f"Generated Code Zip: {zip_file}")
