from django.contrib import admin

from .models import (
    Experiment,
    FoldingResult,
    Generation,
    Mutation,
    Sequence,
)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
        "sequence_length",
        "population_size",
        "random_seed",
        "created_at",
    )

    list_filter = ("status",)
    search_fields = ("name",)


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "experiment",
        "number",
        "created_at",
    )


@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "generation",
        "parent",
        "short_sequence",
        "created_at",
    )

    def short_sequence(self, obj):
        if len(obj.value) <= 40:
            return obj.value

        return f"{obj.value[:40]}..."


@admin.register(Mutation)
class MutationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parent_sequence",
        "child_sequence",
        "position",
        "from_base",
        "to_base",
        "created_at",
    )


@admin.register(FoldingResult)
class FoldingResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sequence",
        "engine",
        "engine_version",
        "free_energy_kcal_mol",
        "created_at",
    )