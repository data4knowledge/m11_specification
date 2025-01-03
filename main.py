from m11_specification import M11Processor

processor = M11Processor(
    template_spec_path="data/input_data/ich-m11-template-step-2b_en.pdf",
    technical_spec_path="data/input_data/ich-m11-technical-specification-step-2b_en.pdf"
)
processor.save_to_json("data/output_data/m11.json")