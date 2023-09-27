import os
import skbuild


def main():
    # Optional: Set the CONDA_PREFIX environment variable to the path of your conda environment
    # Useful if CMAKE can't find the conda environment
    cmake_args = []
    if env_conda := os.getenv("CONDA_PREFIX"):
        cmake_args.append(f"-DCONDA_PREFIX={env_conda}")

    if enable_cuda := os.getenv("DOOZER_ENABLE_CUDA"):
        cmake_args.append(f"-DDOOZER_ENABLE_CUDA={enable_cuda}")

    if enable_nvtx := os.getenv("DOOZER_ENABLE_NVTX"):
        cmake_args.append(f"-DDOOZER_ENABLE_NVTX={enable_nvtx}")

    # Find all python modules in the src directory
    # package_list = find_namespace_packages(where='sleep')
    # print("Found packages:", package_list)

    # Define the python modules to be built
    skbuild.setup(
        name="doozer",
        version="1.0.0",
        description="Python Wrapper for BusySleep",
        packages=["doozer"],
        package_dir={"doozer": "src/doozer"},
        python_requires=">=3.8",
        cmake_args=cmake_args,
    )


if __name__ == "__main__":
    main()
