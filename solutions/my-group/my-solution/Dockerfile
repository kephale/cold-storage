# syntax=docker/dockerfile:1
FROM albumsolutions/album:0.7.1
COPY . /tmp
RUN ["/bin/bash","-c", "sed -i '$ d' /album/src/album/docker/entrypoint.sh ; source /album/src/album/docker/entrypoint.sh ; album install /tmp/album_template-imagej2_0.1.0.zip; sed -i 's/<solution call>/album:template-imagej2:0.1.0/' /album/src/album/docker/entrypoint-solution.sh"]
ENTRYPOINT ["/album/src/album/docker/entrypoint-solution.sh"]
CMD [""]
LABEL MAINTAINER=Album team

