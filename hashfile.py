def hash_file(file, contains_cb, result_cb):
    if contains_cb(file):
        cprint("\tSkipping {}".format(file), "green")
    else:
        try:
            hashes = []
            img = Image.open(file)

            file_size = get_file_size(file)
            image_size = get_image_size(img)
            capture_time = get_capture_time(img)

            # 0 degree hash
            hashes.append(str(dhash(img)))

            # 90 degree hash
            img = img.rotate(90)
            hashes.append(str(dhash(img)))

            # 180 degree hash
            img = img.rotate(180)
            hashes.append(str(dhash(img)))

            # 270 degree hash
            img = img.rotate(270)
            hashes.append(str(dhash(img)))

            hashes = ''.join(sorted(hashes))
            result_cb(file, hashes, file_size, image_size, capture_time)

            cprint("\tHashed {}".format(file), "blue")
        except OSError:
            cprint("Unable to open {}".format(file), "red")

