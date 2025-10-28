from src.shared_kernel.domain._shared import Notification


class TestNotification:
    """
    Test suite for the Notification class.
    """

    def test_initialization(self):
        """
        Test that a newly created Notification has no errors.
        """

        notification = Notification()
        assert not notification.has_errors
        assert notification.messages == ""

    def test_add_error(self):
        """
        Test adding a single error to the Notification.
        """

        notification = Notification()
        notification.add_error("Error 1")
        assert notification.has_errors
        assert notification.messages == "Error 1"

        notification.add_error("Error 2")
        assert notification.has_errors
        assert notification.messages == "Error 1,Error 2"

    def test_multiple_errors(self):
        """
        Test adding multiple errors to the Notification.
        """

        notification = Notification()
        errors = ["Error A", "Error B", "Error C"]
        for error in errors:
            notification.add_error(error)

        assert notification.has_errors
        assert notification.messages == "Error A,Error B,Error C"
