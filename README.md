# About

This repo stores reusable kubernetes manifests for the cqdg project.

The manifests are directly usable non-templated kubernetes manifests which should be fined-tuned using a tool like **kustomize** (now built in **kubectl** either by using the **kustomize** subcommand or passing **-k** flag to **apply**).

# Considered Alternatives

Early in the investigation, there was a bias toward creating helm charts, but after considering of the infrastructure requirements (ie, needing an helm chart repository), added CI complexity (integrating a separate pipeline to release versioned charts, then investigating a third party solution or implementing our own to consume them declaratively) and team-wide cognitive overhead (Go templating), it was decided to use a less powerful, but simpler, less opinionated tool for now.

The above does no preclude using Helm to consume third-party charts (there is a rich ecosystem there) or to change direction for our internal orchestration in the future if there is a need for the powerful features that the tool brings to the table.