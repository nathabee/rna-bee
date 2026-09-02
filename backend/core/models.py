# backend/core/models.py

from django.db import models


class Experiment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    name = models.CharField(max_length=200, blank=True)

    sequence_length = models.PositiveIntegerField()
    population_size = models.PositiveIntegerField(default=1)
    random_seed = models.BigIntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Experiment {self.pk} ({self.status})"


class Generation(models.Model):
    experiment = models.ForeignKey(
        Experiment,
        on_delete=models.CASCADE,
        related_name="generations",
    )

    number = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["experiment", "number"],
                name="unique_generation_per_experiment",
            )
        ]
        ordering = ["number"]

    def __str__(self):
        return f"Experiment {self.experiment_id} / Generation {self.number}"


class Sequence(models.Model):
    generation = models.ForeignKey(
        Generation,
        on_delete=models.CASCADE,
        related_name="sequences",
    )

    value = models.TextField()

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sequence {self.pk}: {self.value[:20]}"


class Mutation(models.Model):
    parent_sequence = models.ForeignKey(
        Sequence,
        on_delete=models.CASCADE,
        related_name="mutations_as_parent",
    )

    child_sequence = models.OneToOneField(
        Sequence,
        on_delete=models.CASCADE,
        related_name="mutation",
    )

    position = models.PositiveIntegerField()

    from_base = models.CharField(max_length=1)
    to_base = models.CharField(max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.from_base}{self.position}{self.to_base} "
            f"({self.parent_sequence_id}->{self.child_sequence_id})"
        )


class FoldingResult(models.Model):
    sequence = models.ForeignKey(
        Sequence,
        on_delete=models.CASCADE,
        related_name="folding_results",
    )

    engine = models.CharField(max_length=100)
    engine_version = models.CharField(max_length=100, blank=True)

    structure = models.TextField()
    free_energy_kcal_mol = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.engine}: Sequence {self.sequence_id}"