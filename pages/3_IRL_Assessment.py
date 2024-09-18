# -*- coding: utf-8 -*-
"""
Copyright (c) Lodve Berre and NTNU Technology Transfer AS 2024.

This file is part of Really Nice IRL.

Really Nice IRL is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
 any later version.

Really Nice IRL is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Really Nice IRL. If not, see:
<https://www.gnu.org/licenses/agpl-3.0.html>.
"""

import streamlit as st
import base
import data_viz
import ui
import utils

from streamlit import session_state as ss


def history_formatter(revision):

    return revision.assessment_date


def on_IRL_val_changed():
    """
    Callback used for all IRL Level sliders.
    Update the session state values.
    Does not save these values to the database.
    """
    ss.project.crl = ss.crl
    ss.project.trl = ss.trl
    ss.project.brl = ss.brl
    ss.project.iprl = ss.iprl
    ss.project.tmrl = ss.tmrl
    ss.project.frl = ss.frl


def on_IRL_target_val_changed():
    """
    Callback used for all IRL Target Level selectors.
    Updates target level values in the session.
    Does not save these values to the database.
    """

    ss.project.crl_target = ss.ass_crl_target
    ss.project.trl_target = ss.ass_trl_target
    ss.project.brl_target = ss.ass_brl_target
    ss.project.iprl_target = ss.ass_iprl_target
    ss.project.tmrl_target = ss.ass_tmrl_target
    ss.project.frl_target = ss.ass_frl_target


def on_history_changed():

    revision = ss.revision
    ss.revision_r = revision


def on_progress_changed():

    r0, r1 = ss.progress_delta
    ss.progress_r0 = r0
    ss.progress_r1 = r1


def on_project_changed():
    """
    Callback for project change.
    Updates current project number and saves to database.
    """

    project_no = ss.project.project_no
    ss.user_settings.last_project_no = int(project_no)
    ss.user_settings.update()
    ss.revision_r = None
    ss.progress_r0 = None
    ss.progress_r1 = None


def on_save_assessment():
    """
    Save updated assessment values to database.
    """
    irl_ass = ss.project

    # Update all values from UI values.
    irl_ass.crl = ss.crl
    irl_ass.trl = ss.trl
    irl_ass.brl = ss.brl
    irl_ass.iprl = ss.iprl
    irl_ass.tmrl = ss.tmrl
    irl_ass.frl = ss.frl
    irl_ass.crl_notes = ss.ass_crl_notes
    irl_ass.trl_notes = ss.ass_trl_notes
    irl_ass.brl_notes = ss.ass_brl_notes
    irl_ass.iprl_notes = ss.ass_iprl_notes
    irl_ass.tmrl_notes = ss.ass_tmrl_notes
    irl_ass.frl_notes = ss.ass_frl_notes
    irl_ass.crl_target = ss.ass_crl_target
    irl_ass.trl_target = ss.ass_trl_target
    irl_ass.brl_target = ss.ass_brl_target
    irl_ass.iprl_target = ss.ass_iprl_target
    irl_ass.tmrl_target = ss.ass_tmrl_target
    irl_ass.frl_target = ss.ass_frl_target
    irl_ass.crl_target_lead = ss.ass_crl_target_lead
    irl_ass.trl_target_lead = ss.ass_trl_target_lead
    irl_ass.brl_target_lead = ss.ass_brl_target_lead
    irl_ass.iprl_target_lead = ss.ass_iprl_target_lead
    irl_ass.tmrl_target_lead = ss.ass_tmrl_target_lead
    irl_ass.frl_target_lead = ss.ass_frl_target_lead
    irl_ass.crl_target_duedate = ss.ass_crl_duedate
    irl_ass.trl_target_duedate = ss.ass_trl_duedate
    irl_ass.brl_target_duedate = ss.ass_brl_duedate
    irl_ass.iprl_target_duedate = ss.ass_iprl_duedate
    irl_ass.tmrl_target_duedate = ss.ass_tmrl_duedate
    irl_ass.frl_target_duedate = ss.ass_frl_duedate

    # ...and save to database...
    irl_ass.update()
    ss.refresh = True


def assessment_view(project, read_only=False):

    # IRL Level Sliders
    st.sidebar.slider("Customer Readiness Level [CRL]",
                      min_value=1,
                      max_value=9,
                      step=1,
                      value=project.crl,
                      key="crl", on_change=on_IRL_val_changed,
                      disabled=read_only)
    st.sidebar.slider("Technology Readiness Level [TRL]",
                      min_value=1,
                      max_value=9,
                      step=1,
                      value=project.trl,
                      key="trl",
                      on_change=on_IRL_val_changed,
                      disabled=read_only)
    st.sidebar.slider("Busines Model Readiness Level [BRL]",
                      min_value=1,
                      max_value=9,
                      step=1,
                      value=project.brl,
                      key="brl",
                      on_change=on_IRL_val_changed,
                      disabled=read_only)
    st.sidebar.slider("IPR Readiness Level [IPRL]",
                      min_value=1,
                      max_value=9,
                      step=1,
                      value=project.iprl,
                      key="iprl",
                      on_change=on_IRL_val_changed,
                      disabled=read_only)
    st.sidebar.slider("Team Readiness Level [TMRL]",
                      min_value=1,
                      max_value=9,
                      step=1,
                      value=project.tmrl,
                      key="tmrl",
                      on_change=on_IRL_val_changed,
                      disabled=read_only)
    st.sidebar.slider("Funding Readiness Level [FRL]",
                      min_value=1,
                      max_value=9,
                      step=1,
                      value=project.frl,
                      key="frl",
                      on_change=on_IRL_val_changed,
                      disabled=read_only)

    # Embed slider values in list for plotting purposes.
    ss['irl_targets'] = [project.crl_target,
                         project.trl_target,
                         project.brl_target,
                         project.iprl_target,
                         project.tmrl_target,
                         project.frl_target]

    # Set up the UI. Viz on the left, descriptions on the right.
    col1, col2 = st.columns([0.5, 0.5])

    with col1:

        header = "<h3 style='text-align: center;'>Innovation Readiness Level<br>%s</h3>"
        st.markdown(header % project, unsafe_allow_html=True)

        if project is not None:

            smooth = ss.user_settings.smooth_irl
            plot_targets = ss.user_settings.plot_target_levels
            dark_mode = ss.user_settings.dark_mode
            fig = data_viz.plot_irl(project,
                                    smooth,
                                    plot_targets,
                                    dark_mode)
            st.pyplot(fig)

            # Target levels and notes.
            if read_only:

                ui.make_action_points('ass', project, None)

            else:

                ui.make_action_points('ass',
                                      project,
                                      on_IRL_target_val_changed)

            st.button("Save assessment",
                      on_click=on_save_assessment,
                      key='trl_action_points',
                      disabled=read_only)

    # Set up all the descriptions and tables.
    with col2:

        ui.irl_explainer()


def history_view(project):
    """
    Display historical IRL assessment values.

    Parameters
    ----------
    project : TYPE
        DESCRIPTION.
    project_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    no_options = len(ss.project_history)
    revision = ss.get('revision_r', None)

    if revision is None or no_options == 1:

        revision = ss.project_history[-1]
        ss.revision_date = revision.assessment_date

    else:

        r = ss.revision_r
        r_index = ss.project_history.index(r)
        r = ss.project_history[r_index]

    if no_options > 1:

        revision = st.sidebar.select_slider("Slide to change project revision",
                                            ss.project_history,
                                            value=revision,
                                            key="revision",
                                            on_change=on_history_changed,
                                            format_func=history_formatter)

    else:

        st.sidebar.radio("Revision:",
                         [revision.assessment_date],
                         key="no_revision")

    if ss.project_history is not None:

        # Set up the UI. Viz on the left, descriptions on the right.
        col1, col2 = st.columns([0.5, 0.5])

        with col1:

            header = "<h3 style='text-align: center;'>Innovation Readiness Level<br>%s</h3>"
            st.markdown(header % ss.project,
                        unsafe_allow_html=True)

            smooth = ss.user_settings.smooth_irl
            dark_mode = ss.user_settings.dark_mode
            plot_targets = ss.user_settings.plot_target_levels
            fig = data_viz.plot_irl(revision,
                                    smooth,
                                    plot_targets,
                                    dark_mode)
            st.pyplot(fig)

        # Set up all the descriptions and tables.
        with col2:

            ui.show_action_points(revision, None)


def progress_view(project):
    """
    Displays the delta between two revisions of a project.

    Parameters
    ----------
    project : TYPE
        DESCRIPTION.
    project_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    no_options = len(ss.project_history)
    r0 = ss.get('progress_r0', None)

    if r0 is None:

        if no_options > 1:

            r0 = ss.project_history[-2]

        else:

            r0 = ss.project_history[0]

        r1 = ss.project_history[-1]

    else:

        r0 = ss.progress_r0
        r1 = ss.progress_r1
        r0_index = ss.project_history.index(r0)
        r1_index = ss.project_history.index(r1)
        r0 = ss.project_history[r0_index]
        r1 = ss.project_history[r1_index]

    if r0 != r1:

        st.sidebar.select_slider(
            "Select revisions to view progress between",
            ss.project_history,
            value=(r0, r1),
            key="progress_delta",
            on_change=on_progress_changed,
            format_func=history_formatter)

    else:

        st.sidebar.radio("Revision:",
                         [r0.assessment_date],
                         key="no_progress_delta",
                         index=0)

    # Set up the UI. Viz on the left, descriptions on the right.
    col1, col2 = st.columns([0.5, 0.5])

    with col1:

        header = "<h3 style='text-align: center;'>Innovation Readiness Level<br>%s</h3>"
        st.markdown(header % ss.project,
                    unsafe_allow_html=True)

        smooth = ss.user_settings.smooth_irl
        dark_mode = ss.user_settings.dark_mode
        fig = data_viz.plot_irl_progress(r0,
                                         r1,
                                         smooth,
                                         dark_mode)
        st.pyplot(fig)

    # Set up all the descriptions and tables.
    with col2:

        ui.show_progress(r0, r1, None)


def main():

    # TODO: Refresh data when user settings changed.
    # Filter on user. Or not.
    if ss.user_settings.filter_on_user:

        user_id = ss.user.user_id

    else:

        user_id = None

    # Disable all submissions if user is only allowed to read.
    utils.get_IRL_data(user_id)

    # Select the last used project initially.
    index = 0
    i = 0
    last_project_no = ss.user_settings.last_project_no

    for project in ss.projects:

        if project.project_no == last_project_no:

            index = i
            break

        i += 1

    # Initialize view state variable.
    if ss.get('irl_view', None) is None:

        ss.irl_view = 'Assessment'

    if len(ss.projects) == 0:

        st.write("You currently do not have any projects. Lucky!")
        return

    st.sidebar.selectbox("Select project:",
                         ss.projects,
                         index=index,
                         key='project',
                         on_change=on_project_changed)

    if ss.project is None:

        project = ss.projects[index]

    else:

        project = ss.project

    project_no = project.project_no
    utils.get_project_history(project_no)
    st.sidebar.radio("View",
                     ["Assessment", "History", "Progress"],
                     key="irl_view",
                     index=0)
    st.sidebar.divider()

    if ss.irl_view == 'Assessment':

        user_rights = ss.user.rights
        project_rights = base.get_project_rights(project_no, ss.user.user_id)
        read_only = (user_rights == 0) or (project_rights == 0)
        assessment_view(project, read_only)

    elif ss.irl_view == 'History':

        history_view(project)

    elif ss.irl_view == 'Progress':

        progress_view(project)


if __name__ == '__main__':

    ui.setup_page()
    # Currently no sensible way to get theme information.
    # We assume dark as this is default until otherwise is proven by user.
    if ss.get('user_settings', None) is None:

        dark_mode = True

    else:

        dark_mode = ss.user_settings.dark_mode

    ui.add_logo(dark_mode)

    # If no user has logged in, force login, remember which page we came from.
    if ss.get('user', None) is None:

        ss['go_to_page'] = 'pages/3_IRL_Assessment.py'
        st.switch_page('pages/2_Login.py')

    else:

        main()
