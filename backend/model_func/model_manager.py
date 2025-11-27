"""
Base model manager and specific model implementations.
"""
import torch
from abc import ABC, abstractmethod
from typing import Optional, Any
from transformers import (
    T5Tokenizer, T5ForConditionalGeneration,
    AutoTokenizer, AutoModelForQuestionAnswering
)
from utils.config_manager import config_manager


class ModelManager(ABC):
    """Abstract base class for model managers."""

    def __init__(self, device: str):
        self.device = device
        self.model: Optional[Any] = None
        self.tokenizer: Optional[Any] = None
        self._load_model()

    @abstractmethod
    def _load_model(self) -> None:
        """Load the model and tokenizer."""
        pass

    def to_device(self) -> None:
        """Move model to device if applicable."""
        if hasattr(self.model, 'to'):
            self.model.to(self.device)
        if hasattr(self.model, 'eval'):
            self.model.eval()


class SummarizerModel(ModelManager):
    """Manager for T5 summarization model."""

    def _load_model(self) -> None:
        try:
            model_dir = config_manager.get_model_dir("summarizer")
            self.tokenizer = T5Tokenizer.from_pretrained(model_dir)
            self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
            self.to_device()
        except Exception as e:
            raise RuntimeError(f"Failed to load summarizer model: {e}")

    def summarize(self, text: str, max_length: int = None) -> str:
        if not text.strip():
            return "No content to summarize"

        if max_length is None:
            max_length = config_manager.max_summary_length

        try:
            input_text = text + " </s>"
            inputs = self.tokenizer(input_text, return_tensors="pt")
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_length=max_length,
                    early_stopping=True
                )

            summary = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            return summary
        except Exception as e:
            raise RuntimeError(f"Summarization failed: {e}")


class TranslatorModel(ModelManager):
    """Manager for T5 translation model."""

    def _load_model(self) -> None:
        try:
            model_dir = config_manager.get_model_dir("translator")
            self.tokenizer = T5Tokenizer.from_pretrained(model_dir)
            self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
            self.to_device()
        except Exception as e:
            raise RuntimeError(f"Failed to load translator model: {e}")

    def translate(self, text: str, max_length: int = None) -> str:
        if not text.strip():
            return "No content to translate"

        if max_length is None:
            max_length = config_manager.max_text_length

        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                max_length=max_length,
                truncation=True
            )
            input_ids = inputs["input_ids"].to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True
                )

            translation = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            return translation
        except Exception as e:
            raise RuntimeError(f"Translation failed: {e}")


class QAModel(ModelManager):
    """Manager for Question Answering model."""

    def _load_model(self) -> None:
        try:
            model_name = config_manager.qa_model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            self.to_device()
        except Exception as e:
            raise RuntimeError(f"Failed to load QA model: {e}")

    def answer_question(self, context: str, question: str) -> str:
        if not context.strip() or not question.strip():
            return "Insufficient context or question"

        try:
            inputs = self.tokenizer(
                question,
                context,
                return_tensors="pt",
                truncation=True
            )
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs.get("attention_mask")
            if attention_mask is not None:
                attention_mask = attention_mask.to(self.device)

            with torch.no_grad():
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )

            answer_start = torch.argmax(outputs.start_logits)
            answer_end = torch.argmax(outputs.end_logits) + 1

            answer = self.tokenizer.convert_tokens_to_string(
                self.tokenizer.convert_ids_to_tokens(
                    input_ids[0][answer_start:answer_end]
                )
            )

            return answer.strip() if answer.strip() else "No answer found in the document"
        except Exception as e:
            raise RuntimeError(f"Question answering failed: {e}")


# Global model instances
summarizer_model = SummarizerModel(config_manager.device)
translator_model = TranslatorModel(config_manager.device)
qa_model = QAModel(config_manager.device)
