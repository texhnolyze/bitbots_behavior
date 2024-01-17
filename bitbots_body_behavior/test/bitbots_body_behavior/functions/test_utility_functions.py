from bitbots_body_behavior.functions.utility_functions import SigmoidTwoXUF


def test_sigmoid_two():
    fn = SigmoidTwoXUF.setup(2, 2)
    assert fn.apply(0) == 1.0
    assert fn.apply(0.2) == 0.9803279976447253
    assert fn.apply(1) == 0.6480542736638855
    assert fn.apply(2) == 0.2658022288340797
