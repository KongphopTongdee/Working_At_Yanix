### Homogeneous model parameters

1. `homoModelParams.json` structure

| Keys | Values |
| - | - |
| logPrior | list: [ P(~HOMO), P(HOMO) ] |
| nonhomo_class | dict( keys:[ 'mean', 'sigma'] ) |
| homo_class | dict( keys:[ 'mean', 'sigma'] ) |


2. `nonhomo_class` & `homo_class` keys in `homoModelParams.json`

| Keys | Values |
| - | :-: |
| mean | list[ $\text{feature}_0[ \mu_Y, \mu_{Cr}, \mu_{Cb} ]$, .&nbsp;.&nbsp;. , $\text{feature}_n[ \mu_Y, \mu_{Cr}, \mu_{Cb} ]$ &nbsp; ]  |
| sigma | list[ feature_0 $\begin{bmatrix}\sigma^2_Y & \sigma_Y\sigma_{Cr} & \sigma_{Y}\sigma_{Cb} \\\sigma_{Cr}\sigma_{Y} & \sigma^2_{Cr} & \sigma_{Cr}\sigma_{Cb}\\\sigma_{Cb}\sigma_{CY} & \sigma_{Cb}\sigma_{Cr} & \sigma^2_{Cb} \end{bmatrix}$ ... feature_n $\begin{bmatrix}\sigma^2_Y & \sigma_Y\sigma_{Cr} & \sigma_{Y}\sigma_{Cb} \\\sigma_{Cr}\sigma_{Y} & \sigma^2_{Cr} & \sigma_{Cr}\sigma_{Cb}\\\sigma_{Cb}\sigma_{CY} & \sigma_{Cb}\sigma_{Cr} & \sigma^2_{Cb} \end{bmatrix}$ ]  |

