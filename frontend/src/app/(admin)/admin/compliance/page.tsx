"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
    complianceService,
    type ComplianceItem,
} from "@/services/campus-services";
import {
    FileCheck,
    Loader2,
    PlayCircle,
    Plus,
    ShieldCheck,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

const COMPLIANCE_TYPES = [
  { value: "declaration", label: "Declaration" },
  { value: "video", label: "Video" },
  { value: "document", label: "Document" },
  { value: "acknowledgement", label: "Acknowledgement" },
];

export default function AdminCompliancePage() {
  const [items, setItems] = useState<ComplianceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    compliance_type: "declaration",
    content_url: "",
    order: 0,
    is_required: true,
  });

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    try {
      const res = await complianceService.listItems();
      setItems(res.items);
    } catch (e: any) {
      toast.error(e.message || "Failed to load compliance items");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!form.title) return;
    setSaving(true);
    try {
      if (editingId) {
        const updated = await complianceService.updateItem(editingId, form);
        setItems((prev) => prev.map((i) => (i.id === editingId ? updated : i)));
        toast.success("Compliance item updated");
      } else {
        const newItem = await complianceService.createItem(form);
        setItems((prev) => [...prev, newItem]);
        toast.success("Compliance item created");
      }
      resetForm();
    } catch (e: any) {
      toast.error(e.message || "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (item: ComplianceItem) => {
    setEditingId(item.id);
    setForm({
      title: item.title,
      description: item.description || "",
      compliance_type: item.compliance_type,
      content_url: item.content_url || "",
      order: item.order,
      is_required: item.is_required,
    });
    setShowForm(true);
  };

  const handleToggleActive = async (item: ComplianceItem) => {
    try {
      const updated = await complianceService.updateItem(item.id, {
        is_active: !item.is_active,
      });
      setItems((prev) => prev.map((i) => (i.id === item.id ? updated : i)));
      toast.success(`Item ${updated.is_active ? "activated" : "deactivated"}`);
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingId(null);
    setForm({
      title: "",
      description: "",
      compliance_type: "declaration",
      content_url: "",
      order: 0,
      is_required: true,
    });
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "declaration":
        return ShieldCheck;
      case "video":
        return PlayCircle;
      case "document":
        return FileCheck;
      default:
        return ShieldCheck;
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-56" />
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <ShieldCheck className="h-7 w-7 text-primary" />
            Compliance Management
          </h1>
          <p className="text-muted-foreground mt-1">
            Create and manage compliance training items for students
          </p>
        </div>
        <Button onClick={() => setShowForm(true)} className="gap-2">
          <Plus className="h-4 w-4" /> New Item
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Total Items</p>
          <p className="text-2xl font-bold mt-1">{items.length}</p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Required</p>
          <p className="text-2xl font-bold mt-1">
            {items.filter((i) => i.is_required).length}
          </p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Active</p>
          <p className="text-2xl font-bold mt-1">
            {items.filter((i) => i.is_active).length}
          </p>
        </div>
      </div>

      {/* Form */}
      {showForm && (
        <div className="glass-card p-6">
          <h3 className="font-semibold text-lg mb-4">
            {editingId ? "Edit Compliance Item" : "Create Compliance Item"}
          </h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="md:col-span-2">
              <label className="text-sm font-medium">Title *</label>
              <Input
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                placeholder="e.g., Anti-Ragging Declaration"
                className="mt-1"
              />
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium">Description</label>
              <textarea
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
                className="w-full mt-1 px-3 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                rows={3}
                placeholder="Enter description or declaration text..."
              />
            </div>
            <div>
              <label className="text-sm font-medium">Type *</label>
              <select
                value={form.compliance_type}
                onChange={(e) =>
                  setForm({ ...form, compliance_type: e.target.value })
                }
                className="w-full mt-1 p-2.5 border rounded-lg bg-background text-sm"
                title="Compliance type"
              >
                {COMPLIANCE_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Order</label>
              <Input
                type="number"
                value={form.order}
                onChange={(e) =>
                  setForm({ ...form, order: Number(e.target.value) })
                }
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">
                Content URL (for videos/documents)
              </label>
              <Input
                value={form.content_url}
                onChange={(e) =>
                  setForm({ ...form, content_url: e.target.value })
                }
                placeholder="https://..."
                className="mt-1"
              />
            </div>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="is_required"
                checked={form.is_required}
                onChange={(e) =>
                  setForm({ ...form, is_required: e.target.checked })
                }
                className="rounded"
              />
              <label htmlFor="is_required" className="text-sm font-medium">
                Required for onboarding
              </label>
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <Button variant="outline" onClick={resetForm}>
              Cancel
            </Button>
            <Button onClick={handleSave} disabled={saving || !form.title}>
              {saving && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
              {editingId ? "Update" : "Create"}
            </Button>
          </div>
        </div>
      )}

      {/* Items List */}
      <div className="space-y-3">
        {items.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <ShieldCheck className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
            <h3 className="text-lg font-semibold mb-2">No Compliance Items</h3>
            <p className="text-muted-foreground">
              Create compliance training items for your students.
            </p>
          </div>
        ) : (
          items
            .sort((a, b) => a.order - b.order)
            .map((item) => {
              const Icon = getTypeIcon(item.compliance_type);
              return (
                <div
                  key={item.id}
                  className={`glass-card p-5 flex items-center gap-4 ${
                    !item.is_active ? "opacity-50" : ""
                  }`}
                >
                  <div className="p-2 rounded-lg bg-primary/10 flex-shrink-0">
                    <Icon className="h-5 w-5 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-sm">{item.title}</h3>
                      {item.is_required && (
                        <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
                          Required
                        </span>
                      )}
                      <span className="text-xs bg-muted px-2 py-0.5 rounded-full capitalize">
                        {item.compliance_type}
                      </span>
                    </div>
                    {item.description && (
                      <p className="text-xs text-muted-foreground mt-1 truncate">
                        {item.description}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(item)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleToggleActive(item)}
                      className={
                        item.is_active ? "text-destructive" : "text-green-600"
                      }
                    >
                      {item.is_active ? "Disable" : "Enable"}
                    </Button>
                  </div>
                </div>
              );
            })
        )}
      </div>
    </div>
  );
}
