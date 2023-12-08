In this study, the authors of the **AAU-PD-T: Aalborg University Person Detection Thermal Dataset** explore the effectiveness of thermal cameras in surveillance, emphasizing their precision in dark environments and privacy preservation. The authors highlight the inefficiency of manual data annotation in the era of data-driven problem-solving and advocate for the importance of a diverse dataset for transfer learning. The investigation involves a comprehensive analysis of a large thermal dataset recorded over 20 weeks, identifying nine distinct phenomena and assessing their impact on model adaptation in transfer learning.

The authors conduct a thorough review of publicly available thermal datasets, particularly focusing on those suitable for person detection. They identify limitations in existing datasets, such as short sequences with limited scene variability, and emphasize the necessity for datasets encompassing diverse weather and light conditions. The discussion notes the scarcity of datasets providing weather information, highlighting one dataset with weather conditions but with limited generalization potential due to its small size.

## **Novel Dataset**

The primary contribution of this paper is the creation and exploration of a diverse thermal dataset for person detection. The dataset, recorded over 20 weeks in outdoor sports fields, addresses challenges related to varying scales, pose variations, interactions between people, and dynamic motions. The dataset spans different weather conditions, from winter snow to spring days, incorporating challenges like varying temperatures, shadows, wind, snow, and occlusions in thermal images. The authors propose nine distinct phenomena crucial for dataset diversity:

<img src="https://github.com/dataset-ninja/aau-pd-t/assets/78355358/ec3ef1d5-c9a3-4975-a4fa-b5249642c672" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">(a) ***low_resolution*** (b) ***far_viewpoint*** (c) ***wind*** (d) ***occlusion*** (e) ***shadow*** (f) ***snow*** (g) ***opposite_temperature*** (h) ***similar_temperature*** (i) ***good_condition***</span>


## **Data Recording**

The authors detail the data acquisition process, involving the recording of thermal videos from 10 different sports fields using Axis Q1921 and Axis 1922 cameras. The cameras, mounted approximately 9 meters above the ground, captured sequences from various perspectives. The recordings spanned from January 2018 to April 2018, totaling 20 weeks of data.

| Category | Phenomena | # of Frames | # of Persons |
| --- | --- | --- | --- |
| Viewpoint | Good condition | 122 | 632 |
| Viewpoint | Far viewpoint | 64 | 652 |
| Heat effects | Opposite temperature | 72 | 792 |
| Heat effects | Similar temperature | 107 | 644 |
| Image artifacts | Low resolution | 158 | 734 |
| Image artifacts | fOcclusion | 20 | 305 |
| Weather effects | Shadow | 171 | 742 |
| Weather effects | Snow | 1060 | 168 |
| Weather effects | Wind | 167 | 921 |

## **Data Description**

To facilitate model adaptation in transfer learning, the authors used 3000 indoor publicly available images for pre-training. The new dataset, designed for generalization in outdoor person detection, was recorded in an outdoor environment and included annotations for all nine identified phenomena. Due to the impracticality of manual annotation for the entire dataset, frames were selected at a temporal gap of 160 seconds, resulting in 1941 frames for the *train* split. *test* split involved randomly selecting 1000 frames from the recorded data, ensuring no overlap with the training set.