from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response, Request, 
    Output, Input, Config
)

class TargetImage(Input):
    name: Literal["targetImage"] = "targetImage"
    value: Union[List[Image], Image]
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
    
    class Config:
        title = "Input Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
    
    class Config:
        title = "Output Image"

class ConfigJpegQuality(Config):
    """
    Sets the JPEG compression quality factor.
    100 is the highest quality (lowest compression), and 0 is the lowest quality (highest compression).
    """
    name: Literal["ConfigJpegQuality"] = "ConfigJpegQuality"
    value: int = Field(default=90, ge=0, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0, 100]"] = "[0, 100]"
    
    class Config:
        title = "JPEG Quality"
        json_schema_extra = {
            "shortDescription": "Compression Quality (0-100)"
        }

class JpegQualityInputs(Inputs):
    targetImage: TargetImage

class JpegQualityConfigs(Configs):
    configJpegQuality: ConfigJpegQuality

class JpegQualityOutputs(Outputs):
    outputImage: OutputImage

class JpegQualityRequest(Request):
    inputs: Optional[JpegQualityInputs]
    configs: JpegQualityConfigs
    
    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class JpegQualityResponse(Response):
    outputs: JpegQualityOutputs

class JpegQuality(Config):
    name: Literal["JpegQuality"] = "JpegQuality"
    value: Union[JpegQualityRequest, JpegQualityResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    
    class Config:
        title = "JPEG Quality Modifier"
        json_schema_extra = {
            "target": {
                "value": 0 
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[JpegQuality]  
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    
    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["ImageQuality"] = "ImageQuality"