FROM python:3.9-alpine

#===============
# Set JAVA_HOME
#===============
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME="/usr/local/openjdk-8"
# RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

#=====================
# Install Android SDK
#=====================
ARG SDK_VERSION=25.2.3
ARG ANDROID_BUILD_TOOLS_VERSION=25.0.3
ENV SDK_VERSION=${SDK_VERSION} \
    ANDROID_BUILD_TOOLS_VERSION=${ANDROID_BUILD_TOOLS_VERSION} \
    ANDROID_HOME="/root"

RUN wget -O tools.zip https://dl.google.com/android/repository/tools_r${SDK_VERSION}-linux.zip && \
    unzip tools.zip && rm tools.zip && \
    chmod a+x -R ${ANDROID_HOME} && \
    chown -R root:root ${ANDROID_HOME}

ENV PATH=${PATH}:${ANDROID_HOME}/tools

RUN echo y | android update sdk -a -u -t platform-tools,build-tools-${ANDROID_BUILD_TOOLS_VERSION}

ENV PATH=${PATH}:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/build-tools

ENV NODE_VERSION 16.17.0

#if build in `china`, debian mirrors, npm registry change to china source
ARG AREA=london

RUN set -ex \
    && if [ 'china' = "$AREA" ] ; then \
        sed -i "s@http://deb.debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list; \
    fi \
    && apt-get update \
    && apt-get install -y git xz-utils curl \

    # install node
    && curl "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz" -O \
    && tar -xf "node-v$NODE_VERSION-linux-x64.tar.xz" \
    && ln -s "/node-v$NODE_VERSION-linux-x64/bin/node" /usr/local/bin/node \
    && ln -s "/node-v$NODE_VERSION-linux-x64/bin/npm" /usr/local/bin/npm \
    && ln -s "/node-v$NODE_VERSION-linux-x64/bin/npx" /usr/local/bin/npx \

    # npm install bump, openapi-generator
    && if [ 'china' = "$AREA" ] ; then \
        npm config set registry https://registry.npm.taobao.org/; \
    fi \
    && npm install -g bump-cli@2.1.0 \
    && ln -s "/node-v$NODE_VERSION-linux-x64/bin/bump" /usr/local/bin/bump \

    # clear
    && npm cache clean --force \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f "/node-v$NODE_VERSION-linux-x64.tar.xz" \
    && apt-get clean \
    && apt-get autoremove

RUN npm install -g appium

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "/app/entry.sh"]