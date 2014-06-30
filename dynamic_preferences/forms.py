from django import forms
from registries import global_preferences_registry, user_preferences_registry, site_preferences_registry

def preference_form_builder(form_base_class, preferences=[], **kwargs):
    """
    Return a form class for updating preferences
    :param form_base_class: a Form class used as the base. Must have a ``registry` attribute
    :param preferences: a list of :py:class:
    :param section: a section where the form builder will load preferences
    """
    registry = form_base_class.registry
    preferences_obj = []
    if len(preferences) > 0:
        # Preferences have been selected explicitly 
        for pref in preferences:
            if type(pref) == str:
                preferences_obj.append(registry.get(name=pref))
            elif type(pref) == tuple:
                preferences_obj.append(registry.get(name=pref[0], section=pref[1]))
            else:
                raise NotImplementedError("The data you provide can't be converted to a Preference object")
    else:
        # Try to use section param
        preferences_obj = registry.preferences(section=kwargs.get('section', None))

    fields = {preference.identifier(): preference.field for preference in preferences_obj}

    form_class = type('CustomGlobalPreferenceForm', (form_base_class,), {'fields': fields})
    return form_class

def global_preference_form_builder(preferences=[], **kwargs):
    """
    A shortcut :py:func:`preference_form_builder(GlobalPreferenceForm, preferences, **kwargs)`
    """
    return preference_form_builder(GlobalPreferenceForm, preferences, **kwargs)

def user_preference_form_builder(preferences=[], **kwargs):
    """
    A shortcut :py:func:`preference_form_builder(UserPreferenceForm, preferences, **kwargs)`
    """
    return preference_form_builder(UserPreferenceForm, preferences, **kwargs)

def site_preference_form_builder(preferences=[], **kwargs):
    """
    A shortcut :py:func:`preference_form_builder(SitePreferenceForm, preferences, **kwargs)`
    """
    return preference_form_builder(SitePreferenceForm, preferences, **kwargs)

class PreferenceForm(forms.Form):

    registry = None

class GlobalPreferenceForm(PreferenceForm):

    registry = global_preferences_registry

class UserPreferenceForm(PreferenceForm):

    registry = user_preferences_registry

class SitePreferenceForm(PreferenceForm):

    registry = site_preferences_registry