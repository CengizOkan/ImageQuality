from sdks.novavision.src.helper.package import PackageHelper
from components.ImageQuality.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    JpegQualityOutputs, JpegQualityResponse, JpegQuality,
    OutputImage
)

def build_response(context):
    output_image = OutputImage(value=context.target_image)
    outputs = JpegQualityOutputs(outputImage=output_image)
    
    executor_response = JpegQualityResponse(outputs=outputs)
    executor = JpegQuality(value=executor_response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)
    
    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )
    package_model = package.build_model(context)
    
    return package_model