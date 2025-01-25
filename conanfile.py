#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
import os

class LibGumboParserConan(ConanFile):
    name = "gumbo-parser"
    version = "0.10.1"
    description = "Gumbo parser - HTML5 parsing library"
    url = "https://github.com/pietermessely/gumbo-parser"
    homepage = "https://github.com/pietermessely/gumbo-parser"
    license = ""
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "visualc/*", "test/*"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
	"with_openssl": [True, False]
    }

    default_options = {
        "shared": False,
        "fPIC": True,
	"with_openssl": True
    }

    def configure(self):
        if(self.settings.compiler != "msvc"):
            del self.settings.compiler.libcxx
            
    def layout(self):
        cmake_layout(self)
        
    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.preprocessor_definitions['BUILD_SHARED_LIBS'] = self.options.shared
        tc.preprocessor_definitions['ENABLE_TESTS'] = False
        tc.preprocessor_definitions['ENABLE_DOCUMENTATION'] = False
        tc.preprocessor_definitions['ENABLE_UTILS'] = False
        tc.preprocessor_definitions['ENABLE_EXAMPLES'] = True
        
        tc.generate()


    #def requirements(self):

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        #cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
        if False:
                
            #self.copy("COPYING", dst="licenses", src=self.source_subfolder, keep_path=False)
            self.copy("*", dst="include", src=os.path.join(self.install_subfolder, "include"))
            self.copy("*.dll", dst="bin", src=os.path.join(self.install_subfolder, "bin"), keep_path=False)
            self.copy("*.dylib", dst="lib", src=os.path.join(self.install_subfolder, "lib"), keep_path=False)
            # rhel installs libraries into lib64
            # cannot use cmake install into package_folder because of lib64 issue
            for libarch in ['lib', 'lib64']:
                arch_dir = os.path.join(self.install_subfolder, libarch)
                cmake_dir_src = os.path.join(arch_dir, "cmake", "libnfs")
                cmake_dir_dst = os.path.join("lib", "cmake", "libnfs")
                pkgconfig_dir_src = os.path.join(arch_dir, "pkgconfig")
                pkgconfig_dir_dst = os.path.join("lib", "pkgconfig")

                self.copy("*.lib", dst="lib", src=arch_dir, keep_path=False)
                self.copy("*.a", dst="lib", src=arch_dir, keep_path=False)
                self.copy("*.so*", dst="lib", src=arch_dir, keep_path=False)
                self.copy("*.*", dst=cmake_dir_dst, src=cmake_dir_src)
                self.copy("*.*", dst=pkgconfig_dir_dst, src=pkgconfig_dir_src)

    def package_info(self):
        self.cpp_info.libs = ["gumbo-parser"]
        if False:
            self.cpp_info.libs = tools.collect_libs(self)

            if self.settings.compiler == "msvc":
                if not self.options.shared:
                    self.cpp_info.libs.append('ws2_32')
    #        elif self.settings.os == "Linux":
