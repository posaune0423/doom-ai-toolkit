"""
Runware Model Upload API Client

This script provides a Python client for uploading models to Runware's platform.
It supports uploading checkpoints, LoRAs, and ControlNet models.
"""

import json
import os
import uuid
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

API_BASE_URL = "https://api.runware.ai/v1"


class RunwareModelUploadClient:
    """Runware API Client for Model Upload"""

    def __init__(self, api_key: Optional[str] = None, timeout_ms: int = 300_000):
        """
        Initialize the Runware client.

        Args:
            api_key: Runware API key. If not provided, will try to load from RUNWARE_API_KEY env var.
            timeout_ms: Request timeout in milliseconds (default: 300 seconds for model uploads)
        """
        self.api_key = api_key or os.getenv("RUNWARE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not provided. Set RUNWARE_API_KEY in .env file or pass api_key parameter."
            )
        self.timeout_ms = timeout_ms

    def upload_checkpoint(
        self,
        download_url: str,
        architecture: str,
        name: str,
        version: str = "1.0",
        type: Optional[str] = None,
        format: str = "safetensors",
        air: Optional[str] = None,
        unique_identifier: Optional[str] = None,
        default_scheduler: Optional[str] = None,
        default_steps: Optional[int] = None,
        default_cfg: Optional[float] = None,
        default_strength: Optional[float] = None,
        private: bool = True,
        hero_image_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
        positive_trigger_words: Optional[List[str]] = None,
        negative_trigger_words: Optional[str] = None,
        short_description: Optional[str] = None,
        comment: Optional[str] = None,
        webhook_url: Optional[str] = None,
        delivery_method: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Upload a checkpoint model to Runware.

        Args:
            download_url: URL where the model file can be downloaded from
            architecture: Model architecture (e.g., "stable-diffusion-xl", "flux")
            name: Model name
            version: Model version (default: "1.0")
            type: Model type (optional)
            format: Model format (default: "safetensors")
            air: AIR identifier (optional, will be auto-generated if not provided)
            unique_identifier: Unique identifier for the model (optional)
            default_scheduler: Default scheduler to use
            default_steps: Default number of steps
            default_cfg: Default CFG scale
            default_strength: Default strength for image-to-image (0-1)
            private: Whether the model should be private (default: True)
            hero_image_url: URL for preview image
            tags: List of tags for the model
            positive_trigger_words: List of positive trigger words
            negative_trigger_words: Comma-separated negative trigger words
            short_description: Short description of the model
            comment: Internal comment/notes
            webhook_url: Webhook URL for async responses
            delivery_method: Delivery method for responses

        Returns:
            List of response dictionaries containing status updates
        """
        task_uuid = str(uuid.uuid4())
        request_data = {
            "taskType": "modelUpload",
            "taskUUID": task_uuid,
            "category": "checkpoint",
            "architecture": architecture,
            "format": format,
            "name": name,
            "version": version,
            "downloadURL": download_url,
            "private": private,
        }

        # Add optional fields
        if type:
            request_data["type"] = type
        if air:
            request_data["air"] = air
        if unique_identifier:
            request_data["uniqueIdentifier"] = unique_identifier
        if default_scheduler:
            request_data["defaultScheduler"] = default_scheduler
        if default_steps is not None:
            request_data["defaultSteps"] = default_steps
        if default_cfg is not None:
            request_data["defaultCFG"] = default_cfg
        if default_strength is not None:
            request_data["defaultStrength"] = default_strength
        if hero_image_url:
            request_data["heroImageURL"] = hero_image_url
        if tags:
            request_data["tags"] = tags
        if positive_trigger_words:
            request_data["positiveTriggerWords"] = positive_trigger_words
        if negative_trigger_words:
            request_data["negativeTriggerWords"] = negative_trigger_words
        if short_description:
            request_data["shortDescription"] = short_description
        if comment:
            request_data["comment"] = comment
        if webhook_url:
            request_data["webhookURL"] = webhook_url
        if delivery_method:
            request_data["deliveryMethod"] = delivery_method

        return self._make_request([request_data])

    def upload_lora(
        self,
        download_url: str,
        architecture: str,
        name: str,
        version: str = "1.0",
        format: str = "safetensors",
        air: Optional[str] = None,
        unique_identifier: Optional[str] = None,
        default_weight: Optional[float] = None,
        private: bool = True,
        hero_image_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
        positive_trigger_words: Optional[List[str]] = None,
        negative_trigger_words: Optional[str] = None,
        short_description: Optional[str] = None,
        comment: Optional[str] = None,
        webhook_url: Optional[str] = None,
        delivery_method: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Upload a LoRA model to Runware.

        Args:
            download_url: URL where the model file can be downloaded from
            architecture: Model architecture (e.g., "stable-diffusion-xl", "flux")
            name: Model name
            version: Model version (default: "1.0")
            format: Model format (default: "safetensors")
            air: AIR identifier (optional, will be auto-generated if not provided)
            unique_identifier: Unique identifier for the model (optional)
            default_weight: Default weight for the LoRA (-4 to 4, default: 1.0)
            private: Whether the model should be private (default: True)
            hero_image_url: URL for preview image
            tags: List of tags for the model
            positive_trigger_words: List of positive trigger words
            negative_trigger_words: Comma-separated negative trigger words
            short_description: Short description of the model
            comment: Internal comment/notes
            webhook_url: Webhook URL for async responses
            delivery_method: Delivery method for responses

        Returns:
            List of response dictionaries containing status updates
        """
        task_uuid = str(uuid.uuid4())
        request_data = {
            "taskType": "modelUpload",
            "taskUUID": task_uuid,
            "category": "lora",
            "architecture": architecture,
            "format": format,
            "name": name,
            "version": version,
            "downloadURL": download_url,
            "private": private,
        }

        # Add optional fields
        if air:
            request_data["air"] = air
        if unique_identifier:
            request_data["uniqueIdentifier"] = unique_identifier
        if default_weight is not None:
            request_data["defaultWeight"] = default_weight
        if hero_image_url:
            request_data["heroImageURL"] = hero_image_url
        if tags:
            request_data["tags"] = tags
        if positive_trigger_words:
            request_data["positiveTriggerWords"] = positive_trigger_words
        if negative_trigger_words:
            request_data["negativeTriggerWords"] = negative_trigger_words
        if short_description:
            request_data["shortDescription"] = short_description
        if comment:
            request_data["comment"] = comment
        if webhook_url:
            request_data["webhookURL"] = webhook_url
        if delivery_method:
            request_data["deliveryMethod"] = delivery_method

        return self._make_request([request_data])

    def upload_controlnet(
        self,
        download_url: str,
        architecture: str,
        conditioning: str,
        name: str,
        version: str = "1.0",
        format: str = "safetensors",
        air: Optional[str] = None,
        unique_identifier: Optional[str] = None,
        private: bool = True,
        hero_image_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
        short_description: Optional[str] = None,
        comment: Optional[str] = None,
        webhook_url: Optional[str] = None,
        delivery_method: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Upload a ControlNet model to Runware.

        Args:
            download_url: URL where the model file can be downloaded from
            architecture: Model architecture (e.g., "stable-diffusion-xl")
            conditioning: Conditioning type (e.g., "canny", "depth", "pose")
            name: Model name
            version: Model version (default: "1.0")
            format: Model format (default: "safetensors")
            air: AIR identifier (optional, will be auto-generated if not provided)
            unique_identifier: Unique identifier for the model (optional)
            private: Whether the model should be private (default: True)
            hero_image_url: URL for preview image
            tags: List of tags for the model
            short_description: Short description of the model
            comment: Internal comment/notes
            webhook_url: Webhook URL for async responses
            delivery_method: Delivery method for responses

        Returns:
            List of response dictionaries containing status updates
        """
        task_uuid = str(uuid.uuid4())
        request_data = {
            "taskType": "modelUpload",
            "taskUUID": task_uuid,
            "category": "controlnet",
            "architecture": architecture,
            "conditioning": conditioning,
            "format": format,
            "name": name,
            "version": version,
            "downloadUrl": download_url,
            "private": private,
        }

        # Add optional fields
        if air:
            request_data["air"] = air
        if unique_identifier:
            request_data["uniqueIdentifier"] = unique_identifier
        if hero_image_url:
            request_data["heroImageUrl"] = hero_image_url
        if tags:
            request_data["tags"] = tags
        if short_description:
            request_data["shortDescription"] = short_description
        if comment:
            request_data["comment"] = comment
        if webhook_url:
            request_data["webhookURL"] = webhook_url
        if delivery_method:
            request_data["deliveryMethod"] = delivery_method

        return self._make_request([request_data])

    def _make_request(self, request_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Make a request to the Runware API and handle streaming responses.

        Args:
            request_data: List of request objects

        Returns:
            List of response dictionaries
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        print(
            f"Uploading model(s)... Task UUID(s): {[r.get('taskUUID') for r in request_data]}"
        )

        try:
            response = requests.post(
                API_BASE_URL,
                headers=headers,
                json=request_data,
                timeout=self.timeout_ms / 1000,  # Convert ms to seconds
                stream=True,  # Enable streaming for status updates
            )

            if not response.ok:
                error_text = response.text
                print(f"Error: {response.status_code} {response.status_text}")
                print(f"Error details: {error_text}")
                response.raise_for_status()

            # Handle streaming responses
            all_responses = []
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        # Try to parse as JSON
                        data = json.loads(line)
                        if isinstance(data, dict) and "data" in data:
                            all_responses.extend(data["data"])
                        elif isinstance(data, list):
                            all_responses.extend(data)
                        else:
                            all_responses.append(data)

                        # Print status updates
                        for item in data.get(
                            "data", [data] if isinstance(data, dict) else []
                        ):
                            if isinstance(item, dict) and "status" in item:
                                status = item.get("status")
                                message = item.get("message", "")
                                air = item.get("air", "")
                                print(f"[{status.upper()}] {message} (AIR: {air})")

                    except json.JSONDecodeError:
                        # If not JSON, might be a plain text response
                        print(f"Received: {line}")

            return all_responses

        except requests.exceptions.Timeout:
            raise TimeoutError(f"Runware API timeout after {self.timeout_ms}ms")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Runware API error: {str(e)}")


def main():
    """Example usage of the Runware Model Upload Client"""
    import argparse

    parser = argparse.ArgumentParser(description="Upload a model to Runware")
    parser.add_argument(
        "--category",
        type=str,
        choices=["checkpoint", "lora", "controlnet"],
        required=True,
        help="Model category",
    )
    parser.add_argument(
        "--url", type=str, required=True, help="Download URL for the model"
    )
    parser.add_argument(
        "--architecture", type=str, required=True, help="Model architecture"
    )
    parser.add_argument("--name", type=str, required=True, help="Model name")
    parser.add_argument("--version", type=str, default="1.0", help="Model version")
    parser.add_argument(
        "--private", action="store_true", default=True, help="Make model private"
    )
    parser.add_argument("--public", action="store_true", help="Make model public")
    parser.add_argument("--tags", type=str, nargs="+", help="Tags for the model")
    parser.add_argument("--description", type=str, help="Short description")
    parser.add_argument(
        "--conditioning", type=str, help="Conditioning type (for ControlNet)"
    )

    args = parser.parse_args()

    client = RunwareModelUploadClient()

    private = args.private and not args.public

    try:
        if args.category == "checkpoint":
            responses = client.upload_checkpoint(
                download_url=args.url,
                architecture=args.architecture,
                name=args.name,
                version=args.version,
                private=private,
                tags=args.tags,
                short_description=args.description,
            )
        elif args.category == "lora":
            responses = client.upload_lora(
                download_url=args.url,
                architecture=args.architecture,
                name=args.name,
                version=args.version,
                private=private,
                tags=args.tags,
                short_description=args.description,
            )
        elif args.category == "controlnet":
            if not args.conditioning:
                parser.error("--conditioning is required for ControlNet models")
            responses = client.upload_controlnet(
                download_url=args.url,
                architecture=args.architecture,
                conditioning=args.conditioning,
                name=args.name,
                version=args.version,
                private=private,
                tags=args.tags,
                short_description=args.description,
            )

        print("\n=== Upload Complete ===")
        print(json.dumps(responses, indent=2))

    except Exception as e:
        print(f"Error uploading model: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
