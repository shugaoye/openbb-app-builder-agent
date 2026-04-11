"""Code generator abstract base class and implementations."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Optional

from .session_manager import Session


class CodeGeneratorConfig:
    """Base configuration for code generators."""

    def __init__(
        self,
        working_directory: Optional[str] = None,
        timeout: float = 600.0,
        **kwargs,
    ):
        """Initialize configuration."""
        self.working_directory = working_directory
        self.timeout = timeout
        self.kwargs = kwargs


class CodeGenerator(ABC):
    """Abstract base class for code generators."""

    @abstractmethod
    async def run(
        self, prompt: str, session: Session, config: CodeGeneratorConfig
    ) -> AsyncGenerator[Dict, None]:
        """Run code generation with the given prompt."""
        pass

    @abstractmethod
    def check_availability(self) -> tuple[bool, str]:
        """Check if the code generator is available."""
        pass


class ClaudeCodeGenerator(CodeGenerator):
    """Claude Code CLI generator implementation."""

    async def run(
        self, prompt: str, session: Session, config: CodeGeneratorConfig
    ) -> AsyncGenerator[Dict, None]:
        """Run Claude Code CLI."""
        from .claude_runner import run_claude_code, ClaudeRunnerConfig

        # Convert to Claude-specific config
        claude_config = ClaudeRunnerConfig(
            working_directory=config.working_directory,
            timeout=config.timeout,
            skip_permissions=config.kwargs.get("skip_permissions", True),
        )

        async for event in run_claude_code(prompt, session, claude_config):
            yield event.data

    def check_availability(self) -> tuple[bool, str]:
        """Check if Claude Code CLI is available."""
        from .config import check_claude_installed

        return check_claude_installed()


class OpenCodeGenerator(CodeGenerator):
    """OpenCode generator implementation."""

    async def run(
        self, prompt: str, session: Session, config: CodeGeneratorConfig
    ) -> AsyncGenerator[Dict, None]:
        """Run OpenCode."""
        # Implement OpenCode integration
        # For now, return a placeholder response
        yield {
            "type": "reasoning",
            "event_type": "INFO",
            "message": "OpenCode generator is not yet implemented",
        }
        yield {
            "type": "message",
            "content": "OpenCode integration is coming soon!",
        }

    def check_availability(self) -> tuple[bool, str]:
        """Check if OpenCode is available."""
        # For now, return that it's not available
        return False, "OpenCode is not yet implemented"


def get_code_generator(generator_type: str) -> CodeGenerator:
    """Get code generator instance based on type."""
    if generator_type == "claude":
        return ClaudeCodeGenerator()
    elif generator_type == "opencode":
        return OpenCodeGenerator()
    else:
        raise ValueError(f"Unknown code generator type: {generator_type}")
