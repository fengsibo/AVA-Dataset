# AVA-Dataset

The [AVA dataset](https://research.google.com/ava/) contains 192 videos split into 154 training and 38 test videos. Each video has 15 minutes annotated in 3 second intervals, resulting in 300 annotated segments. These annotations are specified by two CSV files: [ava_train_v1.0.csv](ava_train_v1.0.csv) and ava_test_v1.0.csv.

Each row contains an annotation for one person performing an action in an interval, where that annotation is associated with the middle frame. Different persons and multiple action labels are described in separate rows.

#### File:
##### ./ava_train_v1.0.csv & ./ava_test_v1.0.csv
The csv files are the label set included eight keys:
- video_id: YouTube identifier
- middle_frame_timestamp: in seconds from the start of the YouTube.
- person_box(x1, y1, x2, y2): top-left (x1, y1) and bottom-right (x2,y2) normalized with respect to frame size, where (0.0, 0.0) corresponds to the top left, and (1.0, 1.0) corresponds to bottom right.
- action_id: identifier of an action class, see ava_action_list_v1.0.pbtxt
- status: the video is availabe

##### ./ava_action_list_v1.0.pbtxt
example:
```
label{
    name: "bend/bow (at the waist)"label_id: 1label_type: PERSON_MOVEMENT
}label{
    name: "crawl"label_id: 2label_type: PERSON_MOVEMENT
}label{
    name: "crouch/kneel"label_id: 3label_type: PERSON_MOVEMENT
}
```


#### Not available video list

train set:

| video_id |
| -------- |
| 2XeFK-DTSZk |
| 4trIFq61-lk |
| EQZWzLyx-GM |
| F_-zE1dQsso |
| G3nRbyu0gMs |
| K--hW14uzA0 |
| ZFQ3lF6yq_E |
| _2Isct32Msg |
| iK4Y-JKRRAc |
| lSCEt_mCHlM |
| ly1upu2FNTs |
| nxL0yqWP3H0 |
| pLJ7bC5Vcqw |
| rXFlJbXyZyc |
| tjqCzVjojCo |

test set:

| video_id |
| -------- |
| XIx-C22Ewk4 |
| bnW1PXGt5hw |
