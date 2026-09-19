#include <dlfcn.h>
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <vulkan/vulkan.h>
#include <vulkan/vk_layer.h>

#define BCN_LAYER_NAME "VK_LAYER_BCN_BCnLayer"

static void *bcn_handle;
static PFN_vkGetInstanceProcAddr bcn_gipa;
static PFN_vkGetDeviceProcAddr bcn_gdpa;

static bool load_bcn_layer(void) {
    if (bcn_gipa && bcn_gdpa) return true;

    setenv("ENABLE_BCN_COMPUTE", "1", 1);
    setenv("BCN_COMPUTE_AUTO", "0", 1);
    setenv("BCN_TRANSCODE_TO_ETC2", "1", 1);
    setenv("BCN_TRANSCODE_TO_ASTC", "0", 1);
    setenv("BCN_LAYER_LOG_LEVEL", "info", 1);
    setenv("BCN_LF", "/data/user/0/com.cuphead/files/bcn_layer.log", 1);

    Dl_info self_info;
    if (!dladdr((void *)&load_bcn_layer, &self_info) || !self_info.dli_fname)
        return false;

    const char *separator = strrchr(self_info.dli_fname, '/');
    if (!separator) return false;

    char path[PATH_MAX];
    size_t directory_length = (size_t)(separator - self_info.dli_fname);
    if (directory_length == 0 || directory_length + sizeof("/libbcn_layer.so") > sizeof(path))
        return false;

    memcpy(path, self_info.dli_fname, directory_length);
    memcpy(path + directory_length, "/libbcn_layer.so", sizeof("/libbcn_layer.so"));

    bcn_handle = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!bcn_handle) return false;

    bcn_gipa = (PFN_vkGetInstanceProcAddr)dlsym(bcn_handle, "BCnLayer_GetInstanceProcAddr");
    bcn_gdpa = (PFN_vkGetDeviceProcAddr)dlsym(bcn_handle, "BCnLayer_GetDeviceProcAddr");
    return bcn_gipa && bcn_gdpa;
}

VKAPI_ATTR VkResult VKAPI_CALL vkEnumerateInstanceLayerProperties(
        uint32_t *property_count, VkLayerProperties *properties) {
    if (!property_count) return VK_ERROR_INITIALIZATION_FAILED;

    const VkLayerProperties property = {
        BCN_LAYER_NAME,
        VK_API_VERSION_1_0,
        1,
        "BCn texture decompression/transcoding layer"
    };

    if (!properties) {
        *property_count = 1;
        return VK_SUCCESS;
    }
    if (*property_count == 0) return VK_INCOMPLETE;

    properties[0] = property;
    *property_count = 1;
    return VK_SUCCESS;
}

VKAPI_ATTR VkResult VKAPI_CALL vkEnumerateInstanceExtensionProperties(
        const char *layer_name, uint32_t *property_count,
        VkExtensionProperties *properties) {
    (void)properties;
    if (!property_count) return VK_ERROR_INITIALIZATION_FAILED;
    if (layer_name && strcmp(layer_name, BCN_LAYER_NAME) != 0)
        return VK_ERROR_LAYER_NOT_PRESENT;
    *property_count = 0;
    return VK_SUCCESS;
}

VKAPI_ATTR VkResult VKAPI_CALL vkEnumerateDeviceLayerProperties(
        VkPhysicalDevice physical_device, uint32_t *property_count,
        VkLayerProperties *properties) {
    (void)physical_device;
    return vkEnumerateInstanceLayerProperties(property_count, properties);
}

VKAPI_ATTR VkResult VKAPI_CALL vkEnumerateDeviceExtensionProperties(
        VkPhysicalDevice physical_device, const char *layer_name,
        uint32_t *property_count, VkExtensionProperties *properties) {
    (void)physical_device;
    return vkEnumerateInstanceExtensionProperties(layer_name, property_count, properties);
}

VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetInstanceProcAddr(
        VkInstance instance, const char *name) {
    if (!strcmp(name, "vkGetInstanceProcAddr"))
        return (PFN_vkVoidFunction)vkGetInstanceProcAddr;
    if (!strcmp(name, "vkEnumerateInstanceLayerProperties"))
        return (PFN_vkVoidFunction)vkEnumerateInstanceLayerProperties;
    if (!strcmp(name, "vkEnumerateInstanceExtensionProperties"))
        return (PFN_vkVoidFunction)vkEnumerateInstanceExtensionProperties;
    if (!load_bcn_layer()) return NULL;
    return bcn_gipa(instance, name);
}

VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetDeviceProcAddr(
        VkDevice device, const char *name) {
    if (!strcmp(name, "vkGetDeviceProcAddr"))
        return (PFN_vkVoidFunction)vkGetDeviceProcAddr;
    if (!load_bcn_layer()) return NULL;
    return bcn_gdpa(device, name);
}

static PFN_vkVoidFunction VKAPI_CALL get_physical_device_proc_addr(
        VkInstance instance, const char *name) {
    return vkGetInstanceProcAddr(instance, name);
}

VKAPI_ATTR VkResult VKAPI_CALL vkNegotiateLoaderLayerInterfaceVersion(
        VkNegotiateLayerInterface *version) {
    if (!version || version->sType != LAYER_NEGOTIATE_INTERFACE_STRUCT)
        return VK_ERROR_INITIALIZATION_FAILED;

    if (version->loaderLayerInterfaceVersion > CURRENT_LOADER_LAYER_INTERFACE_VERSION)
        version->loaderLayerInterfaceVersion = CURRENT_LOADER_LAYER_INTERFACE_VERSION;
    if (version->loaderLayerInterfaceVersion < MIN_SUPPORTED_LOADER_LAYER_INTERFACE_VERSION)
        return VK_ERROR_INITIALIZATION_FAILED;

    version->pfnGetInstanceProcAddr = vkGetInstanceProcAddr;
    version->pfnGetDeviceProcAddr = vkGetDeviceProcAddr;
    version->pfnGetPhysicalDeviceProcAddr = get_physical_device_proc_addr;
    return VK_SUCCESS;
}
