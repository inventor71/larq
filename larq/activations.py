"""Activations can either be used through an `Activation` layer, or through the
`activation` argument supported by all forward layers:

```python
import tensorflow as tf
import larq as lq

model.add(lq.layers.QuantDense(64))
model.add(tf.keras.layers.Activation('hard_tanh'))
```

This is equivalent to:

```python
model.add(lq.layers.QuantDense(64, activation='hard_tanh'))
```

You can also pass an element-wise TensorFlow function as an activation:

```python
model.add(lq.layers.QuantDense(64, activation=lq.activations.hard_tanh))
```
"""

import tensorflow as tf

from larq import utils

__all__ = [
    "HardTanh",
    "HardSigmoid",
]

@utils.register_keras_custom_object
def hard_tanh(x: tf.Tensor, lower_b=-1.0, upper_b=1.0) -> tf.Tensor:
    """Hard tanh activation function.
    ```plot-activation
    activations.hard_tanh
    ```

    # Arguments
        x: Input tensor.
        lower_b: lower bound for hardtanh
        upper_b: upper bound for hardtanh

    # Returns
        Hard tanh activation.
    """
    return tf.clip_by_value(x, lower_b, upper_b)


@utils.register_keras_custom_object
def hard_sigmoid(x: tf.Tensor) -> tf.Tensor:
    """Hard sigmoid activation function.
    ```plot-activation
    activations.hard_sigmoid
    ```

    # Arguments
        x: Input tensor.

    # Returns
        Hard sigmoid activation.
    """
    return tf.clip_by_value(x+0.5, 0.0, 1.0)


@utils.register_keras_custom_object
def leaky_tanh(x: tf.Tensor, alpha: float = 0.2) -> tf.Tensor:
    r"""Leaky tanh activation function.
    Similar to hard tanh, but with non-zero slopes as in leaky ReLU.

    ```plot-activation
    activations.leaky_tanh
    ```

    # Arguments
        x: Input tensor.
        alpha: Slope of the activation function outside of [-1, 1].

    # Returns
        Leaky tanh activation.
    """
    return (
        tf.clip_by_value(x, -1, 1)
        + (tf.math.maximum(x, 1) - 1) * alpha
        + (tf.math.minimum(x, -1) + 1) * alpha
    )


@utils.register_alias("hard_tanh")
@utils.register_keras_custom_object
class HardTanh(tf.keras.layers.Layer):

    def __init__(self, lower_b: float = -1.0, upper_b: float = 1.0, **kwargs):
        self.lower_b = lower_b
        self.upper_b = upper_b
        super().__init__(**kwargs)

    def call(self, inputs):
        return hard_tanh(inputs, lower_b=self.lower_b, upper_b=self.upper_b)

    def get_config(self):
        return {**super().get_config(), "lower_b": self.lower_b, "upper_b": self.upper_b}

    @property
    def non_trainable_weights(self):
        return []

    def compute_output_shape(self, input_shape):
        return input_shape


@utils.register_alias("hard_sigmoid")
@utils.register_keras_custom_object
class HardSigmoid(tf.keras.layers.Layer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, inputs):
        return hard_sigmoid(inputs)

    def get_config(self):
        return {**super().get_config()}

    @property
    def non_trainable_weights(self):
        return []

    def compute_output_shape(self, input_shape):
        return input_shape
