FROM quay.io/pypa/manylinux1_x86_64:latest
# Install libtool and fix paths
RUN yum -y install libtool
RUN for file in /usr/share/aclocal/*.m4; do ln -s /usr/share/aclocal/`basename $file` /usr/local/share/aclocal/`basename $file`; done
# Fix ca-certificates
RUN cp /etc/pki/tls/certs/ca-bundle.crt /root/ca-bundle.crt-old
RUN curl https://curl.haxx.se/ca/cacert.pem -o /etc/pki/tls/certs/ca-bundle.crt
# Build cmake 3 required by libpng
RUN curl -L https://cmake.org/files/v3.9/cmake-3.9.6.tar.gz | tar xzf -
RUN cd cmake-3.9.6 && ./bootstrap && make && make install
RUN which cmake
RUN cmake --version
