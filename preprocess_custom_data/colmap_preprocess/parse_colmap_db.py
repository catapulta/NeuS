# Copyright (c) 2022, ETH Zurich and UNC Chapel Hill.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of ETH Zurich and UNC Chapel Hill nor the names of
#       its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Johannes L. Schoenberger (jsch-at-demuc-dot-de)

import argparse
import sqlite3


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--min_num_matches", type=int, default=15)
    args = parser.parse_args()
    return args

MAX_IMAGE_ID = 2**31 - 1

def pair_id_to_image_ids(pair_id):
    image_id2 = pair_id % MAX_IMAGE_ID
    image_id1 = (pair_id - image_id2) / MAX_IMAGE_ID
    return [image_id1, image_id2]

def image_ids_to_pair_id(image_id1, image_id2):
    if image_id1 > image_id2:
        image_id1, image_id2 = image_id2, image_id1
    return image_id1 * MAX_IMAGE_ID + image_id2

def main():
    args = parse_args()

    connection = sqlite3.connect(args.database_path)
    cursor = connection.cursor()

    img2name = {}
    cursor.execute("SELECT image_id, name FROM images;")
    for row in cursor:
        img2name[row[0]] = row[1]

    used_imgs = set()
    cursor.execute("SELECT pair_id FROM matches;")
    for row in cursor:
        pid2imgid = pair_id_to_image_ids(row[0])
        used_imgs = used_imgs | set([img2name[pid2imgid[0]]])
        used_imgs = used_imgs | set([img2name[pid2imgid[1]]])
    
    print('Number of images in matches table', len(used_imgs))

    used_imgs = set()
    cursor.execute("SELECT pair_id FROM two_view_geometries;")
    for row in cursor:
        pid2imgid = pair_id_to_image_ids(row[0])
        used_imgs = used_imgs | set([img2name[pid2imgid[0]]])
        used_imgs = used_imgs | set([img2name[pid2imgid[1]]])
    
    print('Number of images in two_view_geometries table', len(used_imgs))

    used_imgs = set()
    cursor.execute("SELECT image_id FROM keypoints;")
    for row in cursor:
        used_imgs = used_imgs | set([img2name[row[0]]])
    
    print('Number of images in keypoints table', len(used_imgs))
        
    cursor.execute("SELECT camera_id, model, prior_focal_length FROM cameras;")
    print("Number of cameras", len(list(cursor)))

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()