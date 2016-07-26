## Boaty mcboatface


# How to run.

```
docker build -t mcboatface .
```

and then

```
docker run mcboatface:latest
```

# How to use:

## To get a face representation
```
curl -F "image=@/path/to/image.jpg" host:port/api/v1/face/representation
```
returns:
```
{
  "face": {
    "face_predictor": "shape_predictor_68_face_landmarks.dat",
    "img_dim": 96,
    "network_model": "nn4.small2.v1.t7",
    "representation": [
      -0.018558029085398001,
      0.10032837837934,
      0.0053342413157225002,
      0.016532713547349,
      -0.094650223851204002,
      0.081278592348099005,
      ...
      ],
    }
}

## To get all the face representations
```
curl -F "image=@/path/to/image.jpg" host:port/api/v1/faces/representation
```
returns:
```
{
  "faces": [{...}, {...}],
}
```

## To get similarity between two faces in the image
```
curl -F "image=@/home/user1/Desktop/test.jpg" host:port/api/v1/id_selfie/score
```

returns:
```
{
  "score": 0.993
}
```

# Changes.
Who would want to touch such a magnificent code?
