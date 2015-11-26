__author__ = 'Jaron Horst; based on http://code.activestate.com/recipes/413268/'

######################################################################
##
## Feature Broker
##
######################################################################

class FeatureBroker:
    """
        Main container of DI features.
    """

    def __init__(self):
        self.providers = {}

    def Provide(self, feature, provider, *args, **kwargs):
        """
            Provide a component by name.  Supports optional arguments and/or key-value pairs as well.
        """
        if callable(provider):
            def call():
                return provider(*args, **kwargs)
        else:
            def call():
                return provider
        if (not (feature in self.providers)):
            self.providers[feature] = []
        self.providers[feature].append(call);

    def __getitem__(self, feature):
        """
        :param feature: Name of the features to get from the container
        :return: list of Feature or KeyError
        """
        """
        :param feature:
        :return: list of feature implementations
        """
        try:
            providers = self.providers[feature]
        except KeyError:
            raise KeyError("Unknown feature named "+feature)
        return providers

    def GetFeature(self, feature):
        """
        :param feature: Name of the feature to get from the container
        :return: Feature or KeyError
        """
        """
        :param feature:
        :return:
        """
        try:
            list = self[feature]
            assert len(list) == 1, 'Cannot rerieve only one version of the "'+feature+'" feature - more then one implementation exists.'
            provider = list[0]
        except KeyError:
            raise KeyError("Unknown feature named "+feature)
        return provider()

    def GetFeatures(self, feature):
        """
        :param feature: Name of the features to get from the container
        :return: list of Feature or KeyError
        """
        """
        :param feature:
        :return: list of feature implementations
        """
        return self[feature]
        


features = FeatureBroker()

######################################################################
##
## Representation of Required Features and Feature Assertions
##
######################################################################

#
# Some basic assertions to test the suitability of injected features
#

def NoAssertion(obj):
    """
        No assertion of this object is required.
    """
    return True


def IsInstanceOf(*classes):
    """
        Make sure that a feature is an instance of a specific class type.
    """

    def test(obj): return isinstance(obj, classes)

    return test


def HasAttributes(*attributes):
    """
        Make sure given attributes exist on the class returned.
    """

    def test(obj):
        for each in attributes:
            if not hasattr(obj, each): return False
        return True

    return test


def HasMethods(*methods):
    """
        Make sure given methods exist on the class returned.
    """

    def test(obj):
        for each in methods:
            try:
                attr = getattr(obj, each)
            except AttributeError:
                return False
            if not callable(attr): return False
        return True

    return test


#
# An attribute descriptor to "declare" required features
#

class RequiredFeature(object):
    """
        Get a required feature for a class.
    """

    def __init__(self, feature, assertion=NoAssertion):
        self.feature = feature
        self.assertion = assertion

    def __get__(self, obj, T):
        return self.result  # <-- will request the feature upon first call

    def __getattr__(self, name):
        assert name == 'result', "Unexpected attribute request other then 'result'"
        self.result = self.Request()
        return self.result

    def Request(self):
        obj = features.GetFeature(self.feature)
        assert self.assertion(obj), \
            "The value %r of %r does not match the specified criteria" \
            % (obj, self.feature)
        return obj

    
class RequiredFeatures(object):
    """
        Get a required features list for a class.
    """

    def __init__(self, feature, assertion=NoAssertion):
        self.feature = feature
        self.assertion = assertion

    def __get__(self, obj, T):
        return self.result  # <-- will request the feature upon first call

    def __getattr__(self, name):
        assert name == 'result', "Unexpected attribute request other then 'result'"
        self.result = self.Request()
        return self.result

    def Request(self):
        output = []
        try: # Use a try loop here so we don't error out if nothing is defined for this array!
            objs = features.GetFeatures(self.feature)
            for obj in objs:
                o = obj()
                if (self.assertion(o)):
                    output.append(o)
        except:
            pass
        return output


class Component(object):
    "Symbolic base class for components"