import os
import shutil
import subprocess
import sys


def report_and_check_call(command, *args, **kwargs):
    print('\nCalling: {}'.format(command))
    # may only be required on AppVeyor
    sys.stdout.flush()
    subprocess.check_call(command, *args, **kwargs)


def main():
    build = os.environ['TRAVIS_BUILD_DIR']
    qt_bin_path = os.path.join(build, 'Qt', '5.9.1', 'gcc_64', 'bin')
    destination = os.path.join(build, 'pyqt5-tools')
    os.makedirs(destination, exist_ok=True)

    deployqt_path = os.path.join(
        build,
        'linuxdeployqt',
        'usr',
        'bin',
        'linuxdeployqt',
    )

    applications_to_skip = (
        'fixqt4headers',
        'fixqt4headers.pl',
        'syncqt.pl',
    )

    for application in os.listdir(qt_bin_path):
        if application in applications_to_skip:
            continue

        application_path = os.path.join(qt_bin_path, application)

        shutil.copy(application_path, destination)

        report_and_check_call(
            command=[
                deployqt_path,
                application,
                '-qmake={}'.format(os.path.join(qt_bin_path, 'qmake')),
            ],
            cwd=destination,
        )

    report_and_check_call(
        command=[
            'tree'
        ],
        cwd=destination,
    )


if __name__ == '__main__':
    sys.exit(main())
