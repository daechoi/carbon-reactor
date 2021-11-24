# Stage 1 - the build process
FROM node:14.18-alpine 

WORKDIR /app

# ENV PATH /app/node_modules/.bin:$PATH
# Want to separate dependency installation from the actual edits to our source files

COPY package.json ./
COPY yarn.lock ./

RUN yarn

# add .dockerignore to avoid copying entire current directory
COPY . ./
# start app
CMD ["yarn", "start"]
